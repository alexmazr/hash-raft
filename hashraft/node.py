from .rpc.ServerRPC import ServerRPC
from .rpc.MultiClient import MultiClient
from .cache.SimpleCache import SimpleCache
import yaml
from enum import Enum

class Status (Enum):
    LEADER = "leader"
    FOLLOWER = "follower"
    CANDIDATE = "candidate"

class Node (ServerRPC):
    def __init__ (self, ip, port, name):
        super ().__init__ (ip, port, 1024)
        self.name = name

        with open ("raftConfig.yaml", "r") as stream:
            try:
                config = yaml.safe_load (stream)
            except yaml.YAMLError as e: # What to do on error here?
                print (e)
        self.nodes = MultiClient (Node)
        for k, v in config["nodes"].items ():
            if name != k:
                self.nodes.add (Node, v["ip"], int(v["port"]), 1024, 2)
        self.numberOfNodes = self.nodes.length

        self.cache = SimpleCache ()

        #################################
        # Persistent State
        #################################
        # Node's current term
        self.currentTerm = 0
        # Candidates ID
        self.candidateId = name
        self.votedFor = None
        # Log Entries. Each Entry contains comamnd for state machine, and term when entry was received by leader, first index = 1
        # (a=3, term)
        self.log = [("null", 0)]
        self.lastLogIndex = 0
        self.lastLogTerm = 0
        self.status = Status.FOLLOWER



    def requestVote (self):
        self.status = Status.CANDIDATE
        self.currentTerm += 1
        self.votedFor = self.candidateId

        # Reset heartbeat timer
        results = self.nodes.send_recv.requestVoteHandler (self.currentTerm, self.candidateId, self.lastLogIndex, self.lastLogTerm)
        
        # Calculate vote count
        votesFor = 0
        for vote in results:
            votesFor += 1 if vote [1] else 0

        # Become leader is condition is met
        if votesFor >= self.numberOfNodes // 2 + 1:
            self.status = Status.LEADER
        else:
            self.status = Status.FOLLOWER

    def rpc_triggerRequestVote (self):
        self.requestVote ()
    
    def rpc_requestVoteHandler (self, term, candidateId, lastLogIndex, lastLogTerm):
        # print(f"{self.candidateId} received requestVote from {candidateId}")
        if term < self.currentTerm:
            # print(f"{self.candidateId} rejected {candidateId} as leader")
            return (self.currentTerm, False)
        if (self.votedFor is None or self.votedFor == candidateId) and (lastLogIndex >= self.lastLogIndex):
            # print(f"{self.candidateId} accepted {candidateId} as leader")
            self.votedFor = candidateId
            return (self.currentTerm, True)
    
    def rpc_status (self):
        return {
            "status" : self.status.value,
            "term" : self.currentTerm
        }

    def rpc_ping (self):
        return "200"

    def rpc_pingAll (self):
        status = self.nodes.send_recv.ping ()

        if len (status) != len (self.nodes):
            return "A server is down!"
        for code in status:
            if code != "200":
                return "A server has encountered an error!"
        return "200"

    # Request Vote
    # Vote for me
    # def requestVote (self):
    #     results = self.nodes.send_recv.handleVoteRequest (self.name)

    # def rpc_handleVoteRequest (self, sender):
    #     # I am gonna consider voting for this sender
    #     return False
    
    # def castVote (self):
    #     self.nodes.send.
    
    

    

    def rpc_terminateAll (self):
        self.nodes.send.terminate ()

    def rpc_store (self, key, value):
        self.cache.add (key, value)
    
    def rpc_fetch (self, key):
        return self.cache.get (key)
    
    def rpc_update (self, key, value):
        self.cache.update (key, value)
    
    def rpc_remove (self, key):
        self.cache.remove (key)

    
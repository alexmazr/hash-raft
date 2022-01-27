import json
from . import config
import random as random


class appendEntriesResult:

    term = None
    success = None

    def __init__(self, term, success):
        self.term = term
        self.success = success

class voteResult:

    term = None
    voteGranted = None

    def __init__(self, term, voteGranted):
        self.term = term
        self.voteGranted = voteGranted

class Raft:

    def __init__ (self, candidateId, currentTerm, commitIndex, lastApplied):

        #################################
        # Persistent State
        #################################
        # Node's current term
        self.currentTerm = currentTerm
        # Candidates ID
        self.candidateId = candidateId
        # Log Entries. Each Entry contains comamnd for state machine, and term when entry was received by leader, first index = 1
        # (a=3, term)
        self.log = ["Filler"]

        #################################
        # Volatile State
        #################################
        # index of highest log entry known to be comitted
        self.commitIndex = 0
        # index of highest log entry applied to state machine
        self.lastApplied = 0

        #################################
        # Volatile Leader State
        #################################
        # for each server, index of the next log entry to send to that server (initialized to leader last log index + 1)
        nextIndex = []
        # for each server, index of highest log entry known to be replicated on server (initialized to 0, increases monotonically)
        matchIndex = []

        '''
        Received:
            term:
            voteGranted:
        # Random heartbeat delay 150-300 ms recommended
        self.heartbeatTimeout = random.randint(150, 301)
        1.  Increment my currentTerm
        2. Vote for Node 2
        3. reset heartbeat timer
        4. Send REquest Vote RPC to ALL

        Received Vote request
            if term < self.currentTerm return voteGranted = False
            if votedFor == Null or candidateId AND candidate last log index is up to date grant vote

        ==========
        IF majority comes back with voteGranted = True 
            become LEADER
        IF another leader's heartbeat ping is received
            become FOLLOWER of that leader
        IF heartbeat timer expires start again
        '''
        def requestVote (self):
            self.currentTerm += 1
            self.votedFor = self.candidateId
            # Reset heartbeat timer
            results = self.nodes.send_recv.requestVoteHandler (self.currentTerm, self.candidateId, self.lastLogIndex, self.lastLogTerm)
            votesFor = results.count (True) + 1
            # Change to ciel later
            if votesFor >= self.numberNodes // 2 + 1:
                # Become leader
                print (f"{self.candidateId}} LOOK AT ME, I AM THE CAPTAIN NOW")
            else:
                # Do not become leader
                pass

        
        def rpc_requestVoteHandler (self, term, candidateId, lastLogIndex, lastLogTerm):
            if term < self.currentTerm:
                return (self.currentTerm, False)
            if (self.votedFor is None or self.votedFor == candidateId) and (lastLogIndex >= self.lastLogIndex):
                self.votedFor = candidateId
                return (self.currentTerm, True)


    ####
    #  Would-be remotely invoked call used for leaders to communicate new log entries as well as used for heartbeat pings
    #  in a heartbeat ping entries will be null
    #  TODO: Return statement should be a broadcast to all nodes
    ####
    '''
    1. Client Application makes a commit
    2. Write commit to local log.
    3. Append entry

    def appendEntries(self):
        results = self.nodes.send_recv.appendEntriesHandler(self.myId, self.myLastLogIndex, self.myLastLogTerm, self.entries, self.myLastLogIndex + 1 )
        #

    def rpc_appendEntriesHandler (self, term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
        if term < self.currentTerm:
            return appendEntries(self.currentTerm, False)

        #TODO: Reply false if log doesn’t contain an entry at prevLogIndex whose term matches prevLogTerm
        if self.log[prevLogIndex]is not None and self.log[prevLogIndex][1] != prevLogTerm:
            return False
        
        #TODO: If an existing entry conflicts with a new one (same index but different terms), delete the existing entry and all that follow it 
        if self.log[prevLogIndex]is None or self.log[prevLogIndex][1] != prevLogTerm:
            return False

        #TODO: Append any new entries not already in the log
        #TODO: If leaderCommit > commitIndex, set commitIndex = min(leaderCommit, index of last new entry)

    ####
    #  Would-be remotely invoked call for a leader to replace or install a block of log entries at once 
    ####
    def installSnapshot():
        pass

    def load (self):
        with open(config.SAVEFILE, 'r') as f:
            data = json.load(f)
            self.currentTerm = data["currentTerm"]
            self.candidate = data["candidate"]
            self.myLastLogIndex = data["lastLogIndex"]
            self.myLastLogTerm = data["lastLogTerm"]
            self.votedFor = data["votedFor"]

    ####
    #  Based on Raft specs currentTerm, votedFor and log[] MUST be persisted BEFORE responding to RPC
    ####
    def save (self):
        with open(config.SAVEFILE, 'w') as f:
            data = {}
            data["currentTerm"] = self.currentTerm
            data["candidate"] = self.candidate
            data["lastLogIndex"] = self.myLastLogIndex
            data["lastLogTerm"] = self.myLastLogTerm
            data["votedFor"] = self.votedFor
            json.dump(data, f, indent=2) 

    def getCurrentTerm(self):
        return self.currentTerm

    def getVotedFor(self):
        return self.votedFor
    '''


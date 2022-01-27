from .context import hashraft
from hashraft.rpc.ClientRPC import ClientRPC
from hashraft.node import Node
import threading
import unittest
from timeit import default_timer as timer
import time
import cProfile

class RequestVotesTest (unittest.TestCase):

    def setUp (self):
        nodeList = [Node ("localhost", 8080, 'node1'), Node ("localhost", 8081, 'node2'), Node ("localhost", 8082, 'node3'), Node ("localhost", 8083, 'node4'), Node ("localhost", 8084, 'node5')]
        for node in nodeList:
            threading.Thread (target=node.start, name="serverThread", args=[]).start ()
        self.client = ClientRPC (Node, "localhost", 8080, 1024, 1)

    def tearDown (self):
        self.client.send.terminateAll ()
        self.client.send.terminate ()
        pass

    def test_requestVote (self):
        self.client.send.triggerRequestVote ()
        



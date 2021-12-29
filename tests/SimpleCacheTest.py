from .context import hashraft
from hashraft.rpc.ClientRPC import ClientRPC
from hashraft.node import Node
import threading
import unittest
from timeit import default_timer as timer
import time
import cProfile

class SimpleCacheTest (unittest.TestCase):

    def setUp (self):
        nodeList = [Node ("localhost", 8080, 'node1'), Node ("localhost", 8081, 'node2'), Node ("localhost", 8082, 'node3'), Node ("localhost", 8083, 'node4'), Node ("localhost", 8084, 'node4')]
        for node in nodeList:
            threading.Thread (target=node.start, name="serverThread", args=[]).start ()
        self.client = ClientRPC (Node, "localhost", 8080, 1024, 1)

    def tearDown (self):
        self.client.send.terminateAll ()
        self.client.send.terminate ()
        pass

    def test_add (self):
        self.client.send.store ("dog", "brown")
        self.client.send.store ("cat", "grey")
        self.client.send.store ("bird", 32)

        self.assertEqual (self.client.send_recv.fetch ("dog"), "brown")
        self.assertEqual (self.client.send_recv.fetch ("cat"), "grey")
        self.assertEqual (self.client.send_recv.fetch ("bird"), "32")

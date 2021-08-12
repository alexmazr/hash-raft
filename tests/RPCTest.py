from .context import hashraft
from hashraft.rpc.ClientRPC import ClientRPC
from hashraft.node import Node
import multiprocessing as mp
import threading
import unittest
import time 
from timeit import default_timer as timer

class RPCTest (unittest.TestCase):

    def setUp (self):
        self.node = Node ("localhost", 8080, 'test_node', {})
        server = threading.Thread (target=self.node.start, daemon=True, args=[])
        server.start ()
        self.client = ClientRPC (self.node, 1024, 1)
        time.sleep (0.5)

    def tearDown (self):
        self.client.send.terminate ()

    def test_ping (self):
        self.assertEqual (self.client.send_recv.ping (), "100")

    def testWait (self):
        start = timer ()
        self.client.send.testWait ()
        self.assertEqual (self.client.send_recv.ping (), "100")
        end = timer ()
        # testWait will trigger a function in the server that waits for 2 seconds
        # if we get here and it took 2 seconds or more, this means that the server could
        # not respond to our ping request until testWait was completed. That behaviour would be 
        # faulty, so we test that we can trigger a wait and ping at the same time
        self.assertLess (end-start, 2)
        time.sleep (2)  


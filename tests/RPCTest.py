from .context import hashraft
from hashraft.rpc.ClientRPC import ClientRPC
from hashraft.node import Node
import threading
import unittest

class RPCTest (unittest.TestCase):

    def setUp (self):
        self.node = Node ("localhost", 8080, 'test_node', {})
        thread = threading.Thread (target=self.node.start, daemon=True, args=[])
        thread.start ()
        self.client = ClientRPC (self.node, 1024, 1)

    def tearDown (self):
        self.client.terminate ()

    def test_ping (self):
        self.assertEqual (self.client.ping (), "100")

    def test_noop (self):
        self.client.noop ()

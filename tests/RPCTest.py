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
        nodeList = [Node ("localhost", 8080, 'node1'), Node ("localhost", 8081, 'node2'), Node ("localhost", 8082, 'node3'), Node ("localhost", 8083, 'node4'), Node ("localhost", 8084, 'node4')]
        for node in nodeList:
            threading.Thread (target=node.start, name="serverThread", args=[]).start ()
        self.client = ClientRPC (Node, "localhost", 8080, 1024, 1)

    def tearDown (self):
        self.client.send.terminateAll ()
        self.client.send.terminate ()

    def test_ping (self):
        self.assertEqual (self.client.send_recv.ping (), "200")
    
    def testRpcClientMethodRegistry (self):
        restrictedMethods = ["start", "run", "handler", "process", "callChildMethod", "respond"]
        clientSendMethods = dir(self.client.send)
        clientSendRecvMethods = dir(self.client.send_recv)
        for restricted in restrictedMethods:
            self.assertNotIn (restricted, clientSendMethods)
            self.assertNotIn (restricted, clientSendRecvMethods)

    def testPingAll (self):
        self.assertEqual (self.client.send_recv.pingAll (), "200")


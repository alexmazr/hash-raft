import asyncio
from .rpc.ServerRPC import ServerRPC
from .rpc.ClientRPC import ClientRPC

import time

class Node (ServerRPC):
    def __init__ (self, ip, port, name, nodes):
        super ().__init__ (ip, port, 1024)
        self.name = name
        self.nodes = nodes
        self.clients = []
        for node in nodes:
            if node.name == self.name:
                continue
            self.clients.append (ClientRPC (Node, node.ip, node.port, 1024, 1))
        
    def rpc_ping (self):
        print (self.name + " pinged!")
        return 100

    def noop (self):
        print ("\nhi")

    def rpc_testWait (self):
        time.sleep (2)

    def rpc_pingAll (self):
        print (self.name + " pinging all")
        for client in self.clients:
            client.send.ping ()
        print ("-----------")

    def rpc_terminateAll (self):
        for client in self.clients:
            client.send.terminate ()

    
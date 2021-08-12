from .rpc.ServerRPC import ServerRPC
import time

class Node (ServerRPC):
    def __init__ (self, ip, port, name, nodes):
        super ().__init__ (ip, port, 1024)
        self.name = name
        self.nodes = nodes

    def rpc_ping (self):
        return 100

    def noop (self):
        print ("\nhi")

    def rpc_testWait (self):
        time.sleep (2)
    
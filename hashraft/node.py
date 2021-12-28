import asyncio
from .rpc.ServerRPC import ServerRPC
from .rpc.ClientRPC import ClientRPC
from .rpc.MultiClient import MultiClient
import yaml

import time

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

    def rpc_terminateAll (self):
        self.nodes.send.terminate ()

    
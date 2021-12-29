from hashraft.util.Exceptions import *
from enum import Enum
import socket as so
import time
import random

class RaftState (Enum):
    leader = 1
    follower = 2
    candidate = 3


# TODO: implement raft!

class RaftServer:
    def __init__ (self, name, ip, port, nodes, logger):
        self.name = name
        self.ip = ip
        self.port = port
        self.nodes = nodes
        self.logger = logger
        self.addressStr = str(ip) + ":" + str(port)
        self.currentTerm = 1
        self.termLog = []
        self.state = RaftState.follower

    def create (self):
        self.socket = so.socket ()
        self.socket.setsockopt (so.SOL_SOCKET, so.SO_REUSEADDR, 1)

    def start (self, startEvent):
        self.create ()

        try:
            self.socket.bind ((self.ip, self.port))
            print (self.ip)
        except:
            self.logger.error ("Socket failed to bind for node: " + self.name + " [" + self.addressStr + "]")
            return

        try:
            self.socket.listen ()
        except:
            self.logger.error ("Socket failed to listen for node: " + self.name + " [" + self.addressStr + "]")
            return

        startEvent.set ()
        while (True):
            connection, address = self.socket.accept ()
            connection.settimeout (1)
            try:
                data = connection.recv (1024).decode ()
            except so.timeout:
                self.logger.warning ("A connection was timed out in node: " + self.name + " [" + self.addressStr + "]")

            if not self.dataHandler (data, connection):
                self.socket.shutdown (so.SHUT_RDWR)
                self.socket.close ()
                connection.close ()
                self.logger.warning ("Termination request received at node: " + self.name + " [" + self.addressStr + "]")
                return

            connection.close ()

    def dataHandler (self, data, connection):
        if data == "stop":
            return False
        elif data == "status":
            # time.sleep (random.random ())
            connection.send (b'')
        elif "GET / HTTP" in data:
            connection.send ( str.encode ("HTTP/1.1 403 Forbidden\n\n"))
            connection.shutdown (so.SHUT_RDWR)
        elif "check" in data:
            nodeToCall = data.split(" ")[1]
            socket = so.socket ()
            socket.connect ((self.nodes[nodeToCall]["ip"], self.nodes[nodeToCall]["port"]))
            socket.send (str.encode ("status"))
            socket.settimeout (5)
            try:
                socket.recv (2)
                connection.send ( str.encode ("good"))
            except so.timeout:
                connection.send ( str.encode ("bad"))
        return True


    

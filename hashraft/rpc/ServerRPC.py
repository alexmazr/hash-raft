import socket as so
import threading

class ServerRPC:
    def __init__ (self, ip, port, bufferSize):
        self.ip = ip
        self.port = port
        self.bufferSize = bufferSize
        self.socket = so.socket ()
        self.socket.setsockopt (so.SOL_SOCKET, so.SO_REUSEADDR, 1)
        self.shouldTerminate = False

    def getIp (self):
        return self.ip 
    
    def getPort (self):
        return self.port
    
    def start (self):
        self.socket.bind ((self.ip, self.port))
        self.socket.listen ()
        while (True):
            connection, address = self.socket.accept ()
            connection.settimeout (1)
            data = connection.recv (self.bufferSize).decode ()
            connection.send (str.encode (str(eval ("self." + data))))
            if self.shouldTerminate:
                return
            connection.close ()

    def terminate (self):
        self.socket.shutdown (so.SHUT_RDWR)
        self.socket.close ()
        self.shouldTerminate = True


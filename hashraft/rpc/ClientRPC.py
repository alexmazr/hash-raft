import socket as so

class ClientRPC:

    def __init__ (self, server, bufferSize, timeout):
        method_list = [func for func in dir(server) if callable(getattr(server, func)) and not func.startswith("__")]
        for method in method_list:
            setattr (self, method, self.getLambdaChain (method))

        self.serverIp = server.getIp ()
        self.serverPort = server.getPort ()
        self.timeout = int(timeout)
        self.bufferSize = int(bufferSize)
    
    def getLambdaChain (self, method):
        return lambda *args: self.send_recv (self.connect (), method, *args)
            
    def connect (self):
        socket = so.socket ()
        socket.setsockopt (so.SOL_SOCKET, so.SO_REUSEADDR, 1)
        socket.connect ((self.serverIp, self.serverPort))
        return socket
     
    def send_recv (self, socket, message, *args):
        socket.send (str.encode (message + str(args)))
        socket.settimeout (self.timeout)
        data = socket.recv (self.bufferSize).decode ()
        socket.shutdown (so.SHUT_RDWR)
        socket.close ()
        return data

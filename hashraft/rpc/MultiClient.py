import asyncio
from asyncio.coroutines import coroutine
from typing import Counter
from .ClientRPC import ClientRPC


class MultiClient:
    def __init__ (self, server):
        self.clients = []
        method_list = [func for func in dir(server) if callable(getattr(server, func)) and not func.startswith("__") and func.startswith("rpc_")]
        
        self.send = self.Send (self.clients)
        self.send_recv = self.Send_Recv (self.clients)

        for method in method_list:
            methodName = method[4:]
            setattr (self.send, methodName, self.send.get_Lambda (method))
            setattr (self.send_recv, methodName, self.send_recv.get_Lambda (method))

        self.length = 0
    
    def add (self, Class, ip, port, buffer_size, timeout):
        self.clients.append (ClientRPC (Class, ip, port, buffer_size, timeout))
        self.length += 1
    
    def __len__ (self):
        return self.length

    class Send:
        def __init__ (self, clients):
            self.clients = clients

        def get_Lambda (self, message, *args):
            return lambda *args: self.send_All (message, *args)
        
        def send_All (self, message, *args):
            coroutines = [x.send.send (message) for x in self.clients]
            return asyncio.run (self.internal_gather (coroutines))
        
        async def internal_gather (self, coroutines):
            return await asyncio.gather (*coroutines)
    
    class Send_Recv:
        def __init__ (self, clients):
            self.clients = clients

        def get_Lambda (self, message, *args):
            return lambda *args:self.send_Recv_All (message, *args)

        def send_Recv_All (self, message, *args):
            coroutines = [x.send_recv.send_recv (message) for x in self.clients]
            return asyncio.run (self.internal_gather (coroutines))

        async def internal_gather (self, coroutines):
            return await asyncio.gather (*coroutines)


    
    
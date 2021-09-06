import asyncio
from asyncio.coroutines import coroutine
from typing import Counter


class MultiClient:
    def __init__ (self, clients):
        self.clients = clients
    
    def call_send (self, message):
        coroutines = [x for x in self.clients.send.send (message)]
        return asyncio.run (self.internal_gather (coroutine))

    def call_send_recv (self, message):
        coroutines = [x for x in self.clients.send_recv.send_recv (message)]
        return asyncio.run (self.internal_gather (coroutine))

    async def internal_gather (self, coroutines):
        return await asyncio.gather (*coroutines)

    
    
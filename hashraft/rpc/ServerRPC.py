import asyncio
import threading
from .ServerQueue import CircularBuffer

class ServerRPC:
    def __init__ (self, ip, port, bufferSize):
        self.ip = ip
        self.port = port
        self.bufferSize = bufferSize
        self.queue = CircularBuffer (10)
        self.shouldTerminate = False
        self.server = None
        self.loop = None

    def getIp (self):
        return self.ip 
    
    def getPort (self):
        return self.port

    async def respond (self, writer, response):
        writer.write (response)
        await writer.drain ()
        writer.close ()
        await writer.wait_closed ()

    def callChildMethod (self, data, writer):
        decoded_data = data.decode ()
        response_code = decoded_data[:1]
        to_call = decoded_data[2:]
        response = str (eval ("self." + to_call)).encode ()
        if response_code == "r":
            asyncio.run_coroutine_threadsafe (self.respond (writer, response), self.loop)

    def process (self):
        while (self.server.is_serving ()):
            to_process = self.queue.pop ()
            threading.Thread (target=self.callChildMethod, name="process", daemon=True, args=[to_process["data"], to_process["writer"]]).start ()

    async def handler (self, reader, writer):
        data = await reader.read (self.bufferSize)
        self.queue.push ({"data": data, "writer": writer})

    async def run (self):
        self.loop = asyncio.get_event_loop ()
        self.server = await asyncio.start_server (self.handler, self.ip, self.port, reuse_port=True)
        async with self.server:
            try:
                await asyncio.gather (
                    self.server.serve_forever (), 
                    asyncio.to_thread (self.process)
                )
            except asyncio.exceptions.CancelledError:
                pass
       
    def start (self):
        asyncio.run (self.run ())
    
    async def shutdownRoutine (self):
        self.server.close ()
        await self.server.wait_closed ()
        self.queue.finished ()

    def rpc_terminate (self):
        asyncio.run_coroutine_threadsafe (self.shutdownRoutine (), self.loop)


    # async def messageAll (self):

        


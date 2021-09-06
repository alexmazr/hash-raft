import socket as so
import asyncio 

class ClientRPC:

    def __init__ (self, server, ip, port, bufferSize, timeout):
        method_list = [func for func in dir(server) if callable(getattr(server, func)) and not func.startswith("__") and func.startswith("rpc_")]
        self.send = self.Send (ip, port)
        self.send_recv = self.Send_Recv (ip, port, bufferSize)

        for method in method_list:
            methodName = method[4:]
            setattr (self.send, methodName, self.send.getLambda (method))
            setattr (self.send_recv, methodName, self.send_recv.getLambda (method))

    class Send:
        def __init__ (self, ip, port):
            self.serverIp = ip
            self.serverPort = port

        def getLambda (self, message, *args):
            return lambda *args: asyncio.run (self.send (message, *args))

        async def send (self, message, *args):
            reader, writer = await asyncio.open_connection (self.serverIp, self.serverPort)
            writer.write (("s " + message + str(args)).encode ())
            writer.close ()
            await writer.wait_closed ()
    
    class Send_Recv:
        def __init__ (self, ip, port, bufferSize):
            self.serverIp = ip
            self.serverPort = port
            self.bufferSize = int (bufferSize)

        def getLambda (self, message, *args):
            return lambda *args: asyncio.run (self.send_recv (message, *args))

        async def send_recv (self, message, *args):
            reader, writer = await asyncio.open_connection (self.serverIp, self.serverPort)
            writer.write (("r " + message + str(args)).encode ())
            data = await reader.read (self.bufferSize)
            writer.close()
            await writer.wait_closed ()
            return data.decode ()

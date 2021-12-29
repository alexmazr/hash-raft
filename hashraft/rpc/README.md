# Python 3.9 Async RPC (Remote Procedure Call)
The aim of this readme is to explain how to write your own custom RPC server and client. The provided server and client simply allow you to send or send and recv arbitrary messages (asynchronously). They aren't super useful unless you have created a custom server that inherits `ServerRPC.py`.


- `ServerRPC.py`
    - This is an asynchronous RPC server. It comes out of the box with a remote terminate function and a non-remote start function.
    - Meant to be inherited! Create a custom server class with inheritence. Then simply create remote procedures by following the naming convention `rpc_* (self, args)`. These functions can take any number of remote arguments, and if you'd like the procedure to return a value all you have to do is return it normally.
    - The custom server must also call `super ().__init__ (ip, port, buffer_size)` before you start the server.
- `ClientRPC.py`
    - This client asynchronously sends (or sends and receives) messages.
    - Initialize the client by invoking `ClientRPC (class: Class ref, ip: str, port: int, buffer_size: int, 1)`. Note: The class field must be a reference or object of your custom RPC server, the client uses dynamic dependency injection to create references to remote procedures that are locally callable using dot-notation, no need for strings!
    - How to send a message? (No response)
        - Assume you create a client named `client` and that your custom server has a method called `rpc_noop (self)`
        - You can call this method by simply invoking `client.send.noop ()`
        - Let's say you also have a procedure on your server called `rpc_update (self, data)`
        - You would call it by invoking `client.send.update (data)`
    - How to send and receive a message?
        - Assume you create a client named `client` and that your custom server has a method called `rpc_fetch (self, key)`
        - You can call and wait on a value to be returned by invoking `value = client.send_recv.fetch (key)`. The client will send this message and will block until data is received.

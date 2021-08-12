import threading
class CircularBuffer:
    def __init__ (self, bufferSize):
        self.bufferSize = bufferSize
        self.buffer = [None for x in range (bufferSize)]
        self.pushTo = 0
        self.popFrom = 0
        self.pushEvent = threading.Event ()
        self.popEvent = threading.Event ()
        self.pushLock = threading.Lock ()
        self.popLock = threading.Lock ()
        self.terminated = False
    
    def push (self, item):
        self.pushLock.acquire ()

        if self.terminated:
            return 

        if self.pushTo >= self.bufferSize:
            self.pushTo = 0
            
        # If there is no space to push to, wait for a pop to occur
        while self.buffer[self.pushTo] is not None and not self.terminated:
            self.popEvent.wait (1)

        self.buffer[self.pushTo] = item
        self.pushTo += 1
            
        self.pushEvent.set ()    
        self.pushLock.release ()
    
    def pop (self):
        self.popLock.acquire ()
        
        if self.popFrom >= self.bufferSize:
            self.popFrom = 0

        if self.terminated:
            return
        
        # If there is nothing to pop, wait for a push
        while self.buffer[self.popFrom] is None and not self.terminated:
            self.pushEvent.wait (1)

        poppedItem = self.buffer[self.popFrom]
        self.buffer[self.popFrom] = None
        self.popFrom += 1
        
        self.popEvent.set ()
        self.popLock.release ()
        return poppedItem

    def finished (self):
        self.terminated = True
        self.pushEvent.set ()
        self.popEvent.set ()

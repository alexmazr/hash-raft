import threading
from .LoggingLevel import LoggingLevel
from datetime import datetime
from termcolor import colored



class EventLogger:
    
    def __init__ (self):
        self.mutex = threading.Lock ()
        self.dataLog = []
        self.loggingLevel = LoggingLevel.NONE

    def trace (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [TRACE] " + str(message))
        if self.loggingLevel.value <= LoggingLevel.TRACE.value: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()
    
    def debug (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [DEBUG] " + str(message))
        if self.loggingLevel.value <= LoggingLevel.DEBUG.value: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()

    def info (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [INFO] " + str(message))
        if self.loggingLevel.value <= LoggingLevel.INFO.value: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()
    
    def warning (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [" + colored ("WARN", "yellow") + "] " + str(message))
        if self.loggingLevel.value <= LoggingLevel.WARN.value: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()
    
    def error (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [" + colored ("ERRO", "red") + "] " + str(message))
        if self.loggingLevel.value <= LoggingLevel.ERROR.value: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()
    
    def okay (self, message):
        self.mutex.acquire ()
        date = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        self.dataLog.append (date + " [" + colored ("OKAY", "green") + "] " + str(message))
        if self.loggingLevel.value <= LoggingLevel.OKAY.value: print ("   " + self.getLastEntryNoTime ())
        self.mutex.release ()

    def setLevel (self, level):
        self.loggingLevel = level

    def getLevel (self):
        return self.loggingLevel.name

    def getCurrent (self):
        return self.dataLog
    
    def getCurrentAsString (self):
        return ''.join(self.dataLog)
    
    def getLastEntry (self):
        return str(self.dataLog[-1])
    
    def getLastEntryNoTime (self):
        return str(self.dataLog[-1][20:])
   
    def dump (self):
        self.mutex.acquire ()
        print ()
        for entry in self.dataLog:
            print (entry)
        self.dataLog = []
        self.mutex.release ()
    

from enum import Enum

class LoggingLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    OKAY = 5
    NONE = 6
from enum import Enum

"""
States of client
"""
class StateClient(Enum):
    LOGGING = 1
    CHATTING = 2
    READY = 3
    WAIT = 4
    IDLE = 5
    REQUEST = 6

class Result(Enum):
    OK = 1
    FAILED = 2
    REQUEST = 3
    UNKNOWN = 4

class Boolean(Enum):
    NO = 0
    YES = 1
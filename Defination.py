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
from enum import Enum
from tkinter import CENTER, LEFT, RIGHT


class RequestType(Enum):
    MEMORY_ACCESS = 1
    MOTOR_CONTROL = 2
    COGNITIVE_PROCESS = 3


class ServerType(Enum):
    MOTOR_CONTROL = 1
    COMPLEX_COGNITION = 2
    LONGTERM_MEMORY = 3
    pass


class SubtaskState(Enum):
    """
    The state of the subtask.
    """
    ACTIVE = 0
    HALT = 1

    pass

class SubtaskType(Enum):
    LANEKEEPING = 0
    LANEFOLLOWING = 1
    HAZARD_DETECTION = 2
    INTERSECTION_CROSSING = 3
    REQULATORY = 4
    pass

class GazeDirection(Enum):
    """
    The gaze direction.
    """
    CENTER = 0              # 0.5
    LEFT = 1                # 0.1
    RIGHT = 2               # 0.1
    LEFTBLINDSPOT = 3       # 0.04
    RIGHTBLINDSPOT = 4      # 0.04
    LEFTMIRROR = 5          # 0.08
    RIGHTMIRROR = 6         # 0.08
    BACK = 7                # 0.06
    pass


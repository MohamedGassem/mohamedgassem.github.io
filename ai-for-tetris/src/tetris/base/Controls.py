from enum import Enum, unique, auto


@unique
class Controls(Enum):
    """
        Class that lists possible player actions
    """
    # No action
    NOTHING = auto()
    # Move left
    LEFT = auto()
    # Move right
    RIGHT = auto()
    # Rotate left
    ROTATE_LEFT = auto()
    # Rotate right
    ROTATE_RIGHT = auto()
    # Move down
    DOWN = auto()
    # Store / swap current piece
    STORE = auto()

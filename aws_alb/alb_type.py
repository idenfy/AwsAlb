from enum import auto, Enum


class AlbType(Enum):
    # Loadbalancer is internal and can not be accessed from internet.
    INTERNAL = auto()
    # Loadbalancer is public and can be accessed from internet.
    PUBLIC = auto()

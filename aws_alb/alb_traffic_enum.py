from abc import ABC
from enum import auto


class AlbTrafficEnum(ABC):
    """
    Enum class which tells what type of ingress and egress
    traffic should be applied to application loadbalancer.
    """
    # Allow traffic to/from whole internet.
    INTERNET = auto()
    # Allow traffic to/from within VPC only.
    VPC = auto()
    # Do not allow traffic.
    NONE = auto()

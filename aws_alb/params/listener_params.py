from typing import Optional
from aws_cdk.aws_certificatemanager import CfnCertificate
from aws_cdk.aws_elasticloadbalancingv2 import CfnListener, CfnLoadBalancer
from aws_alb.alb_traffic_enum import AlbTrafficEnum


class ListenerParams:
    """
    Parameters class for loadbalancer listeners.
    """
    def __init__(
            self,
            prefix: str,
            loadbalancer: CfnLoadBalancer,
            port: Optional[int] = None,
            inbound_traffic: AlbTrafficEnum = None,
            outbound_traffic: AlbTrafficEnum = None,
            certificate: Optional[CfnCertificate] = None,
            action: Optional[CfnListener.ActionProperty] = None,
    ) -> None:
        """
        Constructor.

        :param prefix: String prefix for listener name.
        :param loadbalancer: A loadbalancer for which the listener should be configured.
        :param port: Port for listener to listen.
        :param inbound_traffic: Inbound traffic configuration (for security group).
        :param outbound_traffic: Outbound traffic configuration (for security group).
        :param certificate: Certificate to enable https traffic.
        :param action: Action to take when listener gets an incoming traffic.
        """
        self.prefix = prefix
        self.loadbalancer = loadbalancer
        self.port = port
        self.inbound_traffic = inbound_traffic or AlbTrafficEnum.INTERNET
        self.outbound_traffic = outbound_traffic or AlbTrafficEnum.NONE
        self.certificate = certificate
        self.action = action

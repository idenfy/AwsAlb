from typing import Optional
from aws_alb.alb_traffic_enum import AlbTrafficEnum
from aws_cdk.aws_ec2 import SecurityGroup, IVpc, IPeer, Peer
from aws_cdk.core import Stack
from aws_alb.loadbalancer_sg_modifier import SecurityGroupModifier


class LoadBalancerSecurityGroup(SecurityGroup):
    """
    A class which manages a default security group for a loadbalancer.
    """
    def __init__(
            self,
            scope: Stack,
            prefix: str,
            vpc: IVpc,
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation stack in which the resources should be added.
        :param prefix: A prefix for newly created resources.
        :param vpc: Virtual private cloud in which the security groups and a loadbalancer itself should be placed.
        """
        super().__init__(
            scope=scope,
            id=prefix + 'LBSecurityGroup',
            vpc=vpc,
            allow_all_outbound=False,
            description=f'A {prefix} load balancer security group.',
            security_group_name=prefix + 'AppLoadBalancerSG'
        )

        self.__vpc = vpc
        self.__security_group_modifier = SecurityGroupModifier(self)

    def open_port(self, port: int, peer: Optional[IPeer] = None, ingress: bool = True) -> None:
        """
        Modifies a current security group by opening a specified port.

        :param port: Port to open (allow traffic).
        :param peer: Peer (a CIDR or another security group).
        :param ingress: Specifies whether it is configured for ingress or egress traffic.

        :return: No return.
        """
        if peer:
            self.__security_group_modifier.open_port(port, peer, ingress)

    def get_peer(self, traffic: AlbTrafficEnum) -> Optional[IPeer]:
        """
        Depending on enum creates a peer.

        :param traffic: Configuration enum.

        :return: Peer.
        """
        if traffic == AlbTrafficEnum.INTERNET:
            cidr_peer = Peer.any_ipv4()
        elif traffic == AlbTrafficEnum.VPC:
            cidr_peer = Peer.ipv4(self.__vpc.vpc_cidr_block)
        else:
            cidr_peer = None

        return cidr_peer

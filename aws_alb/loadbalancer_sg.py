from aws_cdk import aws_ec2
from aws_cdk.aws_ec2 import SecurityGroup, IVpc, Peer
from aws_cdk.core import Stack
from aws_alb.alb_traffic_enum import AlbTrafficEnum


class LoadBalancerSecurityGroup(SecurityGroup):
    """
    A class which manages a default security group for a loadbalancer.
    """
    def __init__(
            self,
            scope: Stack,
            prefix: str,
            vpc: IVpc,
            https_enabled: bool,
            inbound: AlbTrafficEnum,
            outbound: AlbTrafficEnum
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation stack in which the resources should be added.
        :param prefix: A prefix for newly created resources.
        :param vpc: Virtual private cloud in which the security groups and a loadbalancer itself should be placed.
        :param https_enabled: Boolean telling whether to enable https prots.
        :param inbound: Inbound traffic peers for loadbalancer.
        :param outbound: Outbound traffic peers for loadbalancer.
        """
        super().__init__(
            scope=scope,
            id=prefix + 'LBSG',
            vpc=vpc,
            allow_all_outbound=False,
            description=f'A {prefix} load balancer security group.',
            security_group_name=prefix + 'AppLoadBalancerSG'
        )

        if inbound == AlbTrafficEnum.INTERNET:
            in_cidr = Peer.any_ipv4()
        elif inbound == AlbTrafficEnum.VPC:
            in_cidr = Peer.ipv4(vpc.vpc_cidr_block)
        else:
            in_cidr = None

        if outbound == AlbTrafficEnum.INTERNET:
            out_cidr = Peer.any_ipv4()
        elif outbound == AlbTrafficEnum.VPC:
            out_cidr = Peer.ipv4(vpc.vpc_cidr_block)
        else:
            out_cidr = None

        if in_cidr:
            self.add_ingress_rule(
                peer=in_cidr,
                connection=aws_ec2.Port(
                    protocol=aws_ec2.Protocol.TCP,
                    string_representation=prefix + 'LBSGIngress80',
                    from_port=80,
                    to_port=80
                )
            )

            if https_enabled:
                self.add_ingress_rule(
                    peer=in_cidr,
                    connection=aws_ec2.Port(
                        protocol=aws_ec2.Protocol.TCP,
                        string_representation=prefix + 'LBSGIngress443',
                        from_port=443,
                        to_port=443
                    )
                )

        if out_cidr:
            self.add_egress_rule(
                peer=out_cidr,
                connection=aws_ec2.Port(
                    protocol=aws_ec2.Protocol.TCP,
                    string_representation=prefix + 'LBSGEgress80',
                    from_port=80,
                    to_port=80
                )
            )

            if https_enabled:
                self.add_egress_rule(
                    peer=out_cidr,
                    connection=aws_ec2.Port(
                        protocol=aws_ec2.Protocol.TCP,
                        string_representation=prefix + 'LBSGEgress443',
                        from_port=443,
                        to_port=443
                    )
                )

        def cant_access(**kwargs):
            raise PermissionError('You can not access these methods.')

        # Make sure ingress and egress rules are not modifiable.
        self.add_egress_rule = cant_access
        self.add_ingress_rule = cant_access

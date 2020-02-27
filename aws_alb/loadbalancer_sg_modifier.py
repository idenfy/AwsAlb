from aws_cdk import aws_ec2
from aws_cdk.aws_ec2 import ISecurityGroup, IPeer


class SecurityGroupModifier:
    """
    Class which modifies a given security group.
    """
    def __init__(self, security_group: ISecurityGroup):
        """
        Constructor.

        :param security_group: Security group to modify.
        """
        self.__security_group = security_group

    def open_port(self, port: int, peer: IPeer, ingress: bool = True) -> None:
        """
        Modifies a given security group by opening a specified port.

        :param port: Port to open (allow traffic).
        :param peer: Peer (a CIDR or another security group).
        :param ingress: Specifies whether it is configured for ingress or egress traffic.

        :return: No return.
        """
        assert port is not None
        assert peer is not None
        assert ingress is not None

        sg = self.__security_group

        if ingress:
            sg.add_ingress_rule(
                peer=peer,
                connection=aws_ec2.Port(
                    protocol=aws_ec2.Protocol.TCP,
                    string_representation=f'Ingress {port} rule.',
                    from_port=port,
                    to_port=port
                )
            )
        else:
            sg.add_egress_rule(
                peer=peer,
                connection=aws_ec2.Port(
                    protocol=aws_ec2.Protocol.TCP,
                    string_representation=f'Egress {port} rule.',
                    from_port=port,
                    to_port=port
                )
            )

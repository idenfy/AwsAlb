from typing import Optional, List
from aws_cdk.aws_ec2 import IVpc


class TargetGroupParams:
    """
    Parameters class for target group.
    """
    def __init__(
            self,
            prefix: str,
            vpc: IVpc,
            healthy_http_codes: Optional[List[int]] = None,
            health_check_path: Optional[str] = None,
            target_group_port: int = 80,
            protocol: str = 'HTTP',
            target_type: str = 'ip',
    ) -> None:
        """
        Constructor.

        :param prefix: String prefix for target group name.
        :param vpc: Virtual private cloud for the target group.
        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        :param health_check_path: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a path for that ping.
        :param target_group_port: A port for a communication between loadbalancer and the target group.
        :param protocol: Protocol (http or https).
        :param target_type: Resource in the target group target type (ip or instance).
        """
        self.prefix = prefix
        self.vpc = vpc
        self.healthy_http_codes = healthy_http_codes
        self.health_check_path = health_check_path
        self.target_group_port = target_group_port
        self.protocol = protocol
        self.target_type = target_type

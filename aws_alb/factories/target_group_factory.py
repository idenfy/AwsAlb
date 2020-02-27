from aws_cdk.aws_elasticloadbalancingv2 import CfnTargetGroup
from aws_alb.params.target_group_params import TargetGroupParams
from aws_cdk.core import Stack


class TargetGroupFactory:
    """
    Factory class to create target groups for loadbalancer.
    """
    def __init__(self, scope: Stack) -> None:
        """
        Constructor.

        :param scope: CloudFormation stack instance.
        """
        self.__scope = scope

    def create_target_group(self, target_group_params: TargetGroupParams) -> CfnTargetGroup:
        """
        Creates target group.

        :param target_group_params: Configuration parameters on how to create the target group.

        :return: Target group instance.
        """
        # By default a healthy http code is considered to be 200.
        healthy_http_codes = target_group_params.healthy_http_codes
        healthy_http_codes = [str(code) for code in healthy_http_codes] if healthy_http_codes else ['200']
        healthy_http_codes = ','.join(healthy_http_codes)

        health_check_path = target_group_params.health_check_path

        return CfnTargetGroup(
            self.__scope,
            target_group_params.prefix + 'TargetGroup',
            name=target_group_params.prefix + 'TargetGroup',
            matcher=CfnTargetGroup.MatcherProperty(http_code=healthy_http_codes),
            port=target_group_params.target_group_port,
            protocol=target_group_params.protocol,
            vpc_id=target_group_params.vpc.vpc_id,
            target_type=target_group_params.target_type,
            health_check_path=health_check_path if health_check_path else '/'
        )

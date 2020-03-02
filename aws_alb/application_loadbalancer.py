from typing import List, Optional
from aws_alb.loadbalancer_listeners import LoadBalancerListeners
from aws_cdk import core, aws_ec2
from aws_cdk.aws_certificatemanager import CfnCertificate
from aws_cdk.aws_elasticloadbalancingv2 import CfnLoadBalancer, CfnListener
from aws_alb.loadbalancer_sg import LoadBalancerSecurityGroup


class ApplicationLoadbalancer(CfnLoadBalancer):
    """
    Manager class which creates a loadbalancer and its listeners and security groups and target groups.

    More about loadbalancers:
    https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html
    """
    def __init__(
            self,
            scope: core.Stack,
            prefix: str,
            vpc: aws_ec2.Vpc,
            loadbalancer_subnets: List[aws_ec2.Subnet],
            security_groups: Optional[List[aws_ec2.ISecurityGroup]] = None,
            certificate: Optional[CfnCertificate] = None
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation stack in which the resources should be added.
        :param prefix: A prefix for newly created resources.
        :param vpc: Virtual private cloud in which the security groups and a loadbalancer itself should be placed.
        :param loadbalancer_subnets: Subnets in which the loadbalancer can live.
        :param security_groups: Additional security groups for a loadbalancer.
        """
        self.__loadbalancer_security_group = LoadBalancerSecurityGroup(
            scope=scope,
            prefix=prefix,
            vpc=vpc,
        )

        security_groups = security_groups or []
        security_groups.append(self.__loadbalancer_security_group)

        super().__init__(
            scope,
            prefix + 'AppLoadBalancer',
            security_groups=[sg.security_group_id for sg in security_groups],
            subnets=[subnet.subnet_id for subnet in loadbalancer_subnets],
            type='application',
            scheme='internet-facing',
            name=prefix + 'AppLoadBalancer'
        )

        self.__listeners_manager = LoadBalancerListeners(scope)
        self.__prod_listener, self.__test_listener = self.__listeners_manager.create_default_listeners(
            prefix,
            self,
            certificate
        )

    @property
    def default_prod_listener(self) -> CfnListener:
        return self.__prod_listener

    @property
    def default_test_listener(self) -> CfnListener:
        return self.__test_listener

    @property
    def security_group(self) -> LoadBalancerSecurityGroup:
        """
        Security groups of the loadbalancer.
        More about security groups:
        https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html

        :return: Security groups.
        """
        return self.__loadbalancer_security_group

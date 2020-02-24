from typing import List, Optional
from aws_cdk import core, aws_elasticloadbalancingv2, aws_ec2, aws_certificatemanager
from aws_alb.alb_traffic_enum import AlbTrafficEnum
from aws_alb.loadbalancer_listeners import LoadBalancerListeners
from aws_alb.loadbalancer_sg import LoadBalancerSecurityGroup


class ApplicationLoadbalancer:
    """
    Manager class which creates a loadbalancer and its listeners and security groups.
    """
    def __init__(
            self,
            scope: core.Stack,
            prefix: str,
            vpc: aws_ec2.Vpc,
            loadbalancer_subnets: List[aws_ec2.Subnet],
            security_groups: Optional[List[aws_ec2.ISecurityGroup]] = None,
            inbound_traffic: Optional[AlbTrafficEnum] = None,
            outbound_traffic: Optional[AlbTrafficEnum] = None,
            certificate: Optional[aws_certificatemanager.CfnCertificate] = None
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation stack in which the resources should be added.
        :param prefix: A prefix for newly created resources.
        :param vpc: Virtual private cloud in which the security groups and a loadbalancer itself should be placed.
        :param loadbalancer_subnets: Subnets in which the loadbalancer can live.
        :param security_groups: Additional security groups for a loadbalancer.
        :param inbound_traffic: Inbound traffic for a loadbalancer.
        :param outbound_traffic: Outbound traffic for a loadbalancer.
        :param certificate: To enable HTTPS on a loadbalancer, provide a certificate.

        :return: No return.
        """
        self.__loadbalancer_default_security_group = LoadBalancerSecurityGroup(
            scope=scope,
            prefix=prefix,
            vpc=vpc,
            https_enabled=certificate is not None,
            inbound=inbound_traffic or AlbTrafficEnum.INTERNET,
            outbound=outbound_traffic or AlbTrafficEnum.INTERNET
        )

        security_groups = security_groups or []
        security_groups.append(self.__loadbalancer_default_security_group)

        self.__loadbalancer = aws_elasticloadbalancingv2.CfnLoadBalancer(
            scope,
            prefix + 'AppLoadBalancer',
            security_groups=[sg.security_group_id for sg in security_groups],
            subnets=[subnet.subnet_id for subnet in loadbalancer_subnets],
            type='application',
            scheme='internet-facing',
            name=prefix + 'AppLoadBalancer'
        )

        self.__loadbalancer_default_listeners = LoadBalancerListeners(
            scope=scope,
            prefix=prefix,
            application_loadbalancer=self.__loadbalancer,
            certificate=certificate
        )

    @property
    def loadbalancer(self) -> aws_elasticloadbalancingv2.CfnLoadBalancer:
        """
        Loadbalancer instance.
        More about loadbalancer:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html

        :return: Loadbalancer.
        """
        return self.__loadbalancer

    @property
    def default_listeners(self) -> LoadBalancerListeners:
        """
        Default listeners of the loadbalancer.
        More about listeners:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html

        :return: Listeners.
        """
        return self.__loadbalancer_default_listeners

    @property
    def default_security_group(self) -> LoadBalancerSecurityGroup:
        """
        Default security groups of the loadbalancer.
        More about security groups:
        https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html

        :return: Security groups.
        """
        return self.__loadbalancer_default_security_group

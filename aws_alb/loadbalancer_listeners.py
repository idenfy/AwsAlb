import copy
from typing import Tuple

from aws_alb.alb_traffic_enum import AlbTrafficEnum
from aws_cdk import core
from aws_cdk.aws_elasticloadbalancingv2 import CfnListener, CfnTargetGroup, CfnLoadBalancer
from aws_alb.factories.listener_factory import ListenerFactory
from aws_alb.factories.target_group_factory import TargetGroupFactory
from aws_alb.listener_actions import ListenerActions
from aws_alb.loadbalancer_sg import LoadBalancerSecurityGroup
from aws_alb.params.listener_params import ListenerParams
from aws_alb.params.target_group_params import TargetGroupParams


class LoadBalancerListeners:
    """
    A class which manages listeners for a loadbalancer.
    """
    def __init__(
            self,
            scope: core.Stack,
            prefix: str,
            application_loadbalancer: CfnLoadBalancer,
            loadbalancer_security_group: LoadBalancerSecurityGroup,
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation stack in which the resources should be added.
        :param prefix: A prefix for newly created resources.
        :param application_loadbalancer: Loadbalancer instance.
        :param loadbalancer_security_group: Loadbalancer's security group to manage.
        """
        self.__scope = scope
        self.__prefix = prefix
        self.__application_loadbalancer = application_loadbalancer
        self.__loadbalancer_security_group = loadbalancer_security_group
        self.__available_ports = list(range(20000, 30000))
        self.__listener_factory = ListenerFactory(scope)
        self.__target_group_factory = TargetGroupFactory(scope)
        
    def create_blue_green(
            self,
            listener_params: ListenerParams,
            target_group_params: TargetGroupParams
    ) -> Tuple[Tuple[CfnTargetGroup, CfnListener], Tuple[CfnTargetGroup, CfnListener]]:
        """
        Creates listeners and target groups for out-of-the-box blue green deployments with AWS CodeDeploy.

        :param listener_params:
        :param target_group_params:

        :return: Tuple with two tuples. First tuple contains a blue pair and the second group contains a green pair.
        A pair contains two elements: a target group and a listener.
        """
        assert listener_params.port is None, 'You can not specify port when creating multiple listeners.'
        assert listener_params.action is None, 'You can not specify action when creating multiple listeners.'

        blue_target_group_params = copy.deepcopy(target_group_params)
        green_target_group_params = copy.deepcopy(target_group_params)

        blue_listener_params = copy.deepcopy(listener_params)
        green_listener_params = copy.deepcopy(listener_params)

        blue_target_group_params.prefix = blue_target_group_params.prefix + 'Blue'
        green_target_group_params.prefix = green_target_group_params.prefix + 'Green'

        blue_group = self.create_target_group(blue_target_group_params)
        green_group = self.create_target_group(green_target_group_params)

        blue_listener_params.prefix = blue_listener_params.prefix + 'Blue'
        blue_listener_params.action = ListenerActions.target_group_action(blue_group)
        blue_listener_params.port = self.__allocate_port()
        green_listener_params.prefix = green_listener_params.prefix + 'Green'
        green_listener_params.action = ListenerActions.target_group_action(green_group)
        green_listener_params.port = self.__allocate_port()

        blue_listener = self.create_listener(blue_listener_params)
        green_listener = self.create_listener(green_listener_params)
        
        return (blue_group, blue_listener), (green_group, green_listener)

    def create_listener(self, listener_params: ListenerParams) -> CfnListener:
        """
        Creates a listener for a loadbalancer.

        :param listener_params: Configuration parameters for the new listener.

        :return: Listener instance.
        """
        inbound = self.__loadbalancer_security_group.get_peer(listener_params.inbound_traffic)
        outbound = self.__loadbalancer_security_group.get_peer(listener_params.outbound_traffic)

        self.__loadbalancer_security_group.open_port(listener_params.port, inbound, ingress=True)
        self.__loadbalancer_security_group.open_port(listener_params.port, outbound, ingress=False)

        return self.__listener_factory.create(listener_params)

    def create_target_group(self, target_group_params: TargetGroupParams) -> CfnTargetGroup:
        """
        Creates a target group.

        :param target_group_params: Configuration parameters for the new target group.

        :return: Target group instance.
        """
        return self.__target_group_factory.create_target_group(target_group_params)

    def __allocate_port(self) -> int:
        """
        Allocates a free available port for a listener.

        :return: Available port.
        """
        return self.__available_ports.pop(0)

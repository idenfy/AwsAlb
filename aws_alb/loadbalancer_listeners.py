from typing import Tuple, Optional
from aws_cdk import core
from aws_cdk.aws_certificatemanager import CfnCertificate
from aws_cdk.aws_elasticloadbalancingv2 import CfnListener, CfnTargetGroup, CfnLoadBalancer
from aws_alb.factories.listener_factory import ListenerFactory
from aws_alb.factories.target_group_factory import TargetGroupFactory
from aws_alb.listener_actions import ListenerActions
from aws_alb.params.listener_params import ListenerParams
from aws_alb.params.target_group_params import TargetGroupParams


class LoadBalancerListeners:
    """
    A class which manages listeners for a loadbalancer.
    """

    def __init__(self, scope: core.Stack) -> None:
        """
        Constructor.

        :param scope: A CloudFormation stack in which the resources should be added.
        """
        self.__listener_factory = ListenerFactory(scope)
        self.__target_group_factory = TargetGroupFactory(scope)

    def create_default_listeners(
            self,
            prefix: str,
            loadbalancer: CfnLoadBalancer,
            cert: Optional[CfnCertificate] = None
    ) -> Tuple[CfnListener, CfnListener]:
        """
        Creates default listeners for normal loadbalancer use.
        If certificate is provided, creates listeners for 80, 8000, 443, 44300 ports.
        If certificate is not provided, creates listeners for 80, 8000 ports.

        Listener 80 redirects to 443 and listener 8000 redirects to 44300 in case certificate is provided.

        :param prefix: A string prefix for resources.
        :param loadbalancer: Attach listeners to given loadbalancer.
        :param cert: Certificate to enable https.

        :return: Tuple of two listeners. First one is blue (production) and the second one is green (test).
        """
        blue = None
        green = None

        if cert:
            blue = self.create_listener(ListenerParams(
                prefix + 'BlueHttps',
                loadbalancer,
                certificate=cert,
                port=443,
                action=ListenerActions.fixed_404_action()
            ))

            green = self.create_listener(ListenerParams(
                prefix + 'GreenHttps',
                loadbalancer,
                certificate=cert,
                port=44300,
                action=ListenerActions.fixed_404_action()
            ))

        blue_http = self.create_listener(ListenerParams(
            prefix + 'BlueHttp',
            loadbalancer,
            port=80,
            action=ListenerActions.redirect_action(blue.port) if cert else ListenerActions.fixed_404_action()
        ))

        green_http = self.create_listener(ListenerParams(
            prefix + 'GreenHttp',
            loadbalancer,
            port=8000,
            action=ListenerActions.redirect_action(green.port) if cert else ListenerActions.fixed_404_action()
        ))

        blue = blue or blue_http
        green = green or green_http

        return blue, green

    def create_blue_green(
            self,
            blue_listener_params: ListenerParams,
            green_listener_params: ListenerParams,
            blue_target_group_params: TargetGroupParams,
            green_target_group_params: TargetGroupParams
    ) -> Tuple[Tuple[CfnTargetGroup, CfnListener], Tuple[CfnTargetGroup, CfnListener]]:
        """
        Creates listeners and target groups for out-of-the-box blue green deployments with AWS CodeDeploy.

        :param blue_listener_params: Listener parameters for the blue group.
        :param green_listener_params: Listener parameters for the green group.
        :param blue_target_group_params:  Target group parameters for the blue group.
        :param green_target_group_params: Target group parameters for the green group.

        :return: Tuple with two tuples. First tuple contains a blue pair and the second group contains a green pair.
        A pair contains two elements: a target group and a listener.
        """
        # Ensure prefixes tell which is green and which is blue.
        blue_target_group_params.prefix = blue_target_group_params.prefix + 'Blue'
        blue_listener_params.prefix = blue_listener_params.prefix + 'Blue'
        green_target_group_params.prefix = green_target_group_params.prefix + 'Green'
        green_listener_params.prefix = green_listener_params.prefix + 'Green'

        # Create target groups and forward to them.
        blue_group = self.create_target_group(blue_target_group_params)
        blue_listener_params.action = ListenerActions.target_group_action(blue_group)
        green_group = self.create_target_group(green_target_group_params)
        green_listener_params.action = ListenerActions.target_group_action(green_group)

        # Create listeners.
        blue_listener = self.create_listener(blue_listener_params)
        green_listener = self.create_listener(green_listener_params)

        return (blue_group, blue_listener), (green_group, green_listener)

    def create_listener(self, listener_params: ListenerParams) -> CfnListener:
        """
        Creates a listener for a loadbalancer.

        :param listener_params: Configuration parameters for the new listener.

        :return: Listener instance.
        """
        sg = listener_params.loadbalancer.security_group

        inbound = sg.get_peer(listener_params.inbound_traffic)
        outbound = sg.get_peer(listener_params.outbound_traffic)

        sg.open_port(listener_params.port, inbound, ingress=True)
        sg.open_port(listener_params.port, outbound, ingress=False)

        return self.__listener_factory.create(listener_params)

    def create_target_group(self, target_group_params: TargetGroupParams) -> CfnTargetGroup:
        """
        Creates a target group.

        :param target_group_params: Configuration parameters for the new target group.

        :return: Target group instance.
        """
        return self.__target_group_factory.create_target_group(target_group_params)

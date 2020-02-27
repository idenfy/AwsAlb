from aws_cdk.aws_elasticloadbalancingv2 import CfnListener
from aws_cdk.core import Stack
from aws_alb.listener_actions import ListenerActions
from aws_alb.params.listener_params import ListenerParams


class ListenerFactory:
    """
    Factory class which creates listeners for loadbalancer.
    """
    def __init__(self, scope: Stack) -> None:
        """
        Constructor.

        :param scope: CloudFormation stack instance.
        """
        self.__scope = scope

    def create(self, listener_params: ListenerParams) -> CfnListener:
        """
        Creates listener.

        :param listener_params: Configuration parameters on how to create the listener.

        :return: Listener instance.
        """
        protocol = 'HTTPS' if listener_params.certificate else 'HTTP'

        listener = CfnListener(
            scope=self.__scope,
            id=listener_params.prefix + f'{protocol.capitalize()}Listener{listener_params.port}',
            port=listener_params.port,
            protocol=protocol,
            load_balancer_arn=listener_params.loadbalancer.ref,
            default_actions=[listener_params.action or ListenerActions.fixed_404_action()]
        )

        if listener_params.certificate:
            listener.certificates = [
                CfnListener.CertificateProperty(certificate_arn=listener_params.certificate.ref)
            ]

        return listener

from aws_cdk.aws_elasticloadbalancingv2 import CfnListener, CfnTargetGroup


class ListenerActions:
    """
    Factory class to create various actions for loadbalancer listeners.
    """
    @staticmethod
    def redirect_action(port: int, protocol: str = 'HTTPS'):
        """
        Creates redirect action to same host with same path and query
        but to different port with different protocol.

        :param port: Port to redirect to.
        :param protocol: Protocol to use.

        :return: Redirect action.
        """
        return CfnListener.ActionProperty(
            type='redirect',
            redirect_config=CfnListener.RedirectConfigProperty(
                status_code='HTTP_301',
                host='#{host}',
                path='/#{path}',
                port=str(port),
                query='#{query}',
                protocol=protocol
            )
        )

    @staticmethod
    def target_group_action(target_group: CfnTargetGroup) -> CfnListener.ActionProperty:
        """
        Creates forward action to a target group.

        :param target_group: Target group to forward to.

        :return: Forward action.
        """
        return CfnListener.ActionProperty(
            type='forward',
            target_group_arn=target_group.ref
        )

    @staticmethod
    def fixed_404_action() -> CfnListener.ActionProperty:
        """
        Creates fixed 404 (not found) response.

        :return: Fixed 404 response action.
        """
        return CfnListener.ActionProperty(
            type='fixed-response',
            fixed_response_config=CfnListener.FixedResponseConfigProperty(
                status_code='404',
                message_body='Not found.'
            )
        )

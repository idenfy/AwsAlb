from typing import Optional
from aws_cdk import core, aws_elasticloadbalancingv2, aws_certificatemanager


class LoadBalancerListeners:
    """
    A class which manages default listeners for a loadbalancer.
    """
    LISTENER_HTTP_PORT_1 = 80
    LISTENER_HTTPS_PORT_1 = 443
    LISTENER_HTTP_PORT_2 = 8000
    LISTENER_HTTPS_PORT_2 = 44300

    def __init__(
            self,
            scope: core.Stack,
            prefix: str,
            application_loadbalancer: aws_elasticloadbalancingv2.CfnLoadBalancer,
            certificate: Optional[aws_certificatemanager.CfnCertificate]
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation stack in which the resources should be added.
        :param prefix: A prefix for newly created resources.
        :param application_loadbalancer: Loadbalancer instance.
        :param certificate: A certificate for a loadbalancer to enable https.
        """
        self.__certificate = certificate

        self.__listener_http_1 = None
        self.__listener_https_1 = None
        self.__listener_http_2 = None
        self.__listener_https_2 = None

        self.__not_found_404_action = aws_elasticloadbalancingv2.CfnListener.ActionProperty(
            type='fixed-response',
            fixed_response_config=aws_elasticloadbalancingv2.CfnListener.FixedResponseConfigProperty(
                status_code='404',
                message_body='Not found.'
            )
        )

        self.__listener_http_1 = aws_elasticloadbalancingv2.CfnListener(
            scope, prefix + 'HttpListener1',
            port=self.LISTENER_HTTP_PORT_1,
            protocol='HTTP',
            load_balancer_arn=application_loadbalancer.ref,
            default_actions=[
                aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='redirect',
                    redirect_config=aws_elasticloadbalancingv2.CfnListener.RedirectConfigProperty(
                        status_code='HTTP_301',
                        host='#{host}',
                        path='/#{path}',
                        port=str(self.LISTENER_HTTPS_PORT_1),
                        query='#{query}',
                        protocol='HTTPS'
                    )
                ) if certificate else self.__not_found_404_action
            ]
        )

        if certificate:
            self.__listener_https_1 = aws_elasticloadbalancingv2.CfnListener(
                scope, prefix + 'HttpsListener1',
                certificates=[aws_elasticloadbalancingv2.CfnListener.CertificateProperty(
                    certificate_arn=certificate.ref
                )],
                port=self.LISTENER_HTTPS_PORT_1,
                protocol='HTTPS',
                load_balancer_arn=application_loadbalancer.ref,
                default_actions=[self.__not_found_404_action]
            )

        self.__listener_http_2 = aws_elasticloadbalancingv2.CfnListener(
            scope, prefix + 'HttpListener2',
            port=self.LISTENER_HTTP_PORT_2,
            protocol='HTTP',
            load_balancer_arn=application_loadbalancer.ref,
            default_actions=[
                aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='redirect',
                    redirect_config=aws_elasticloadbalancingv2.CfnListener.RedirectConfigProperty(
                        status_code='HTTP_301',
                        host='#{host}',
                        path='/#{path}',
                        port=str(self.LISTENER_HTTPS_PORT_2),
                        query='#{query}',
                        protocol='HTTPS'
                    )
                ) if certificate else self.__not_found_404_action
            ]
        )

        if certificate:
            self.__listener_https_2 = aws_elasticloadbalancingv2.CfnListener(
                scope, prefix + 'HttpsListener2',
                certificates=[aws_elasticloadbalancingv2.CfnListener.CertificateProperty(
                    certificate_arn=certificate.ref
                )],
                port=self.LISTENER_HTTPS_PORT_2,
                protocol='HTTPS',
                load_balancer_arn=application_loadbalancer.ref,
                default_actions=[self.__not_found_404_action]
            )

    @property
    def https_enabled(self) -> bool:
        """
        Tells whether https is enabled or not for a loadbalancer.

        :return: Boolean for whether https is enabled.
        """
        return self.__certificate is not None

    @property
    def production_http_listener(self) -> aws_elasticloadbalancingv2.CfnListener:
        """
        Listener instance for serving http traffic.

        :return: Http listener.
        """
        return self.__listener_http_1

    @property
    def production_https_listener(self) -> Optional[aws_elasticloadbalancingv2.CfnListener]:
        """
        Listener instance for serving https traffic.

        :return: Https listener.
        """
        return self.__listener_https_1

    @property
    def deployments_http_listener(self) -> aws_elasticloadbalancingv2.CfnListener:
        """
        Listener instance for serving test http traffic.

        :return: Test http listener.
        """
        return self.__listener_http_2

    @property
    def deployments_https_listener(self) -> Optional[aws_elasticloadbalancingv2.CfnListener]:
        """
        Listener instance for serving test https traffic.

        :return: Test https listener.
        """
        return self.__listener_https_2

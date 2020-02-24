## AWS ALB (Application Load Balancer)

An abstract application loadbalancer construct. It creates a loadbalancer and default
security groups and listeners for the loadbalancer. Also, this loadbalancer is ready
for blue-green deployments.

#### Remarks

The project is written by [Laimonas Sutkus](https://github.com/laimonassutkus) 
and is owned by [iDenfy](https://github.com/idenfy). This is an open source
library intended to be used by anyone. [iDenfy](https://github.com/idenfy) aims
to share its knowledge and educate market for better and more secure IT infrastructure.

#### Related technology

This project utilizes the following technology:

- *AWS* (Amazon Web Services).
- *AWS CDK* (Amazon Web Services Cloud Development Kit).
- *AWS CloudFormation*.
- *AWS Loadbalancer*.
- *AWS Security groups*.

#### Assumptions

This library project assumes the following:

- You have knowledge in AWS (Amazon Web Services).
- You have knowledge in AWS CloudFormation and AWS loadbalancing.
- You are managing your infrastructure with AWS CDK.
- You are writing AWS CDK templates with a python language.

#### Install

The project is built and uploaded to PyPi. Install it by using pip.

```bash
pip install aws-alb
```

Or directly install it through source.

```bash
./build.sh -ic
```

#### Description

It is usually hard to create a loadbalancer following best practices and rules. Also, most of the 
time the deployed loadbalancer will lack some configuration functionality for deployment management.
We tackle these problems by providing you a library to easily deploy and maintain a loadbalancer with
right security groups, right listeners and most importantly right configuration for blue-green deployments.

#### Examples

To create an application loadbalancer create an `ApplicationLoadbalancer`
instance in your stack. An example is given below:

```python
from aws_cdk import core, aws_ec2
from aws_alb.alb_traffic_enum import AlbTrafficEnum
from aws_alb.application_loadbalancer import ApplicationLoadbalancer

class MainStack(core.Stack):
    def __init__(self, scope: core.App) -> None:
        super().__init__(
            scope=scope,
            id='MyCoolStack'
        )
        
        # Create your own vpc.
        self.vpc = aws_ec2.Vpc(
            self,
            'MyCoolVpc'
        )

        self.public_http_loadbalancer = ApplicationLoadbalancer(
            scope=self,
            prefix='MyCool',
            vpc=self.vpc,
            loadbalancer_subnets=self.vpc.public_subnets,
            security_groups=None,
            inbound_traffic=AlbTrafficEnum.INTERNET,
            outbound_traffic=AlbTrafficEnum.INTERNET,
            certificate=None
        )
```

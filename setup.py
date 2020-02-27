from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='aws_alb',
    version='2.0.0',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(exclude=['venv', 'test']),
    description=(
        'AWS CDK package that creates a highly opinionated application load balancer.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        'aws_cdk.core',
        'aws_cdk.aws_elasticloadbalancingv2',
        'aws_cdk.aws_certificatemanager',
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@gmail.com (laimonas@idenfy.com)',
    keywords='AWS CDK ALB ELB LoadBalancer',
    url='https://github.com/idenfy/AwsAlb.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

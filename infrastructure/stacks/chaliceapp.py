import os

from aws_cdk import (
    core as cdk,
    aws_sns as sns, 
    aws_sns_subscriptions as sns_subscriptions,
    aws_lambda as _lambda,
    aws_iam as iam
)
from chalice.cdk import Chalice


API_HANDLER_RUNTIME = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.pardir, 'wp-api-lambda')

SNS_HANDLER_RUNTIME = os.path.join(
os.path.dirname(os.path.dirname(__file__)), os.pardir, 'wp-sns-lambda')

class WhatsappBotStack(cdk.Stack):

    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.topic = sns.Topic(self, "'whatsapp-bot-command-topic",
            display_name="test whatsapp lambda topic"
        )
        self.role = iam.Role.from_role_arn(self, "WhatsappBotRole", 
                                           role_arn="arn:aws:iam::923699018646:role/wp-bot-dev",
                                           mutable=False)
        self.api_handler = Chalice(self, 'WhatsappAckAPIHandler', 
                                   source_dir=API_HANDLER_RUNTIME,
                                   stage_config={
                                       'environment_variables': {
                                           'TOPIC_ARN': self.topic.topic_arn,
                                       }
                                   })
        self.sns_lambda = _lambda.DockerImageFunction(self, "WhatsappCommandHandler",
                          code=_lambda.DockerImageCode.from_image_asset(SNS_HANDLER_RUNTIME),
                          role=self.role)

        self.topic.add_subscription(sns_subscriptions.LambdaSubscription(self.sns_lambda))

import os

from aws_cdk import (
    core as cdk,
    aws_sns as sns, 
    aws_sns_subscriptions as sns_subscriptions,
    aws_lambda as _lambda,
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
        self.api_handler = Chalice(self, 'WhatsappAckAPIHandler', 
                                   source_dir=API_HANDLER_RUNTIME,
                                   stage_config={
                                       'environment_variables': {
                                           'TOPIC_ARN': self.topic.topic_arn,
                                       }
                                   })
        self.sns_lambda = _lambda.Function(
            self, 'WhatsappCommandHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='app.handler',
            code=_lambda.Code.from_asset(SNS_HANDLER_RUNTIME)
        )
        self.topic.add_subscription(sns_subscriptions.LambdaSubscription(self.sns_lambda))

# class ChaliceSNS(cdk.Stack):

#     def __init__(self, scope, id, **kwargs):
#         super().__init__(scope, id, **kwargs)
#         self.sns_handler = Chalice(self, 'WhatsappSNSHandler', source_dir=RUNTIME_FOR_OTHER_LAMBDA)
#         self.topic = sns.Topic(self, "'my-demo-topic",
#             display_name="test whatsapp lambda topic"
#         )


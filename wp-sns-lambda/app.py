import boto3
import json
import os

from utils.secrets import get_binance_secret, get_twilio_secret
from utils.twilio import get_twilio_message
# from utils.commands import 


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    account_sid, auth_token = get_twilio_secret()
    try:
        twilio = TwilioClient(account_sid, auth_token) 
        message = twilio.messages.create( 
            from_=message.get('Receiver'),
            body=response_bodies[random.randint(0,9)],      
            to=message.get('Sender').get('Number')
        ) 
    except TwilioException as e:
        
    
    for record in event:

        message = json.loads(record["Sns"]["Message"])

        body = {"Hello": "World"}

        print('downstream response: {}'.format(body))
        return json.loads(body)

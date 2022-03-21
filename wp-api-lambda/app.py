import boto3
import json
import logging
import os

from chalice import Chalice, Response

from chalicelib.twilio import get_twilio_message
from chalicelib.utils import validate_command


app = Chalice(app_name='wp-bot-platform')
logging.basicConfig(level = logging.INFO)
app.log.setLevel(logging.DEBUG)

sns = boto3.client('sns')

@app.route('/ping')
def index():
    app.log.info('logging cloudfront using chalice log')
    return {'data': 'pong'}


@app.route('/whatsapp/ack', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def WhatsappAckHandler():
    message = get_twilio_message(app.current_request.raw_body)
    
    if not validate_command(message.get('Body')):
        app.log.info('Message %s is not a command %s', (message.get('MessageSid'), message.get('Body')))
        return

    app.log.info('Processing incoming message from twilio %s', message)
    try:
        sns.publish(Message=json.dumps(message), 
                    Subject='MessageIsACommand',
                    TopicArn=os.environ['TOPIC_ARN'])
    except Exception as e:
        app.log.error(f'Something wrong happened - {str(e)}')
        return Response(
            body={"error": str(e)},
            status_code=500,
            headers={'Content-Type': 'application/json'}
        )
    else:
        return Response(
            body={},
            status_code=200,
            headers={'Content-Type': 'application/json'}
        )

import json
import logging

from utils.secrets import get_twilio_secret
from utils.commands import process_command
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioException


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_sns_message(event):
    if 'Records' not in event:
        logger.error('Invalid event payload.', exc_info=True)
        return
    logger.info(f'Number of sns event records: {len(event.get("Records"))}')
    for record in event.get('Records'):
        yield json.loads(record["Sns"]["Message"])


def handler(event, context):
    account_sid, auth_token = get_twilio_secret()
    for message in get_sns_message(event):
        logger.info('Processing incoming message from twilio %s', message)
        
        command_in = message.get("Body")
        try:
            command_out = process_command(command_in)
        except Exception as e:
            logger.error('Error processing command %s', e)
        
        logger.info('Processing command output %s', command_out)
        try:
            twilio = TwilioClient(account_sid, auth_token) 
            message = twilio.messages.create( 
                from_=message.get('Receiver'),
                body=command_out,      
                to=message.get('Sender').get('Number')
            ) 
        except TwilioException as e:
            error = {
                'name': str(e),
                'uri': e.uri,
                'status': e.status,
                'message': e.msg,
                'code': e.code,
                'method': e.method,
                'details': e.details,
            }
            logger.error('Twilio error: %s', error)
        else:
            logger.info("Message processed successfully")

import boto3
import json
import logging

from botocore.exceptions import ClientError


def get_binance_secret():

    secret = _get_secret("wp-bot/BinanceSecrets")
    api_key = secret.get('BinanceApiKey')
    secret_key = secret.get('BinanceSecretKey')
    
    if not api_key or not secret_key:
        logging.error('[get_binance_secret] Impossibility to retrieve the secrets: %s', secret)

    return api_key, secret_key


def get_twilio_secret():

    secret = _get_secret("wp-bot/TwilioSecrets")
    account_sid = secret.get('AccountSid')
    auth_token = secret.get('AuthToken')

    if not account_sid or not auth_token:
        logging.error('[get_twilio_secret] Impossibility to retrieve the secrets: %s', secret)

    return account_sid, auth_token


def _get_secret(name, region="us-east-1"):

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=name
        )
    except ClientError as e:
        logging.error('[_get_secret] Something happening retrieving the secrets %s', repr(e))
        raise e
    except Exception as e:
        logging.error('[_get_secret] Unknown exception - %s', repr(e))
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret_string = get_secret_value_response['SecretString']
        else:
            logging.error('[_get_secret] No secrets string in aws response')
            return None, None

    return json.loads(secret_string)

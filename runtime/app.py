import logging
import random

from binance.client import Client
from chalice import Chalice, Response
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioException

from chalicelib.secrets import get_binance_secret, get_twilio_secret
from chalicelib.twilio import get_twilio_message

app = Chalice(app_name='wp-bot-platform')
logging.basicConfig(level = logging.INFO)
app.log.setLevel(logging.DEBUG)

@app.route('/ping')
def index():
    app.log.info('logging cloudfront using chalice log')
    return {'data': 'pong'}

@app.route('/coin/{coin}', methods=['GET'])
def CoinUSDTHandler(coin=None):

    API_KEY, SECRET_KEY = get_binance_secret()
    client = Client(API_KEY, SECRET_KEY)
    symbol = coin + 'USDT' if coin else 'BTCUSDT'
    app.log.info('Fetching %s price', symbol)
    try:
        avg_price = client.get_avg_price(symbol=symbol)
    except Exception as e:
        app.log.error('Something happened fetching %s symbol from Binance', symbol)
        raise e 
    response = {
        'price': avg_price.get('price')
    }

    return  response

@app.route('/whatsapp/ack', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def WhatsappAckHandler():
    account_sid, auth_token = get_twilio_secret()
    message = get_twilio_message(app.current_request.raw_body)
    
    app.log.info('Processing incoming message from twilio %s', message)
    response_bodies = [
        "todo bien por aqui",
        "que paso pana mio",
        "que tal va tu dia",
        "Hola soy un bot", 
        "Que quieres hacer hoy?",
        "La puta que te pario",
        "Como te llamas",
        "La concha de la lora",
        "Disculpa no quise insultarte",
        "Espero que estes bien"
    ]
    try:
        twilio = TwilioClient(account_sid, auth_token) 
        message = twilio.messages.create( 
            from_=message.get('Receiver'),
            body=response_bodies[random.randint(0,9)],      
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
        app.log.error('Twilio error: %s', error)
        return Response(body=error,
                        status_code=500,
                        headers={'Content-Type': 'application/json'})
    except Exception as e:
        error = {'error': str(e)}
        app.log.error('Unknown Exception - %s', error)
        return Response(body=error,
                        status_code=500,
                        headers={'Content-Type': 'application/json'})
    else:
        app.log.info('Message created: message_id=%s', message)
        return Response(body={},
                        status_code=204,
                        headers={'Content-Type': 'application/json'})

from services.binance import get_price_variation

def process_command(message):
    """
    Example command: '\pv month BNB,BTC,ETH'
    """
    try:
        command, interval, coins = message.split()
    except ValueError:
        raise Exception("Invalid command: Command has not three parts")

    handlers = {
        "\pv": get_price_variation, 
    }

    message = handlers[command](interval, coins)

    return message

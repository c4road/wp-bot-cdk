def is_valid_command(message):
    """
    Validate a message is a command
    :params str message: the message body
    example command:  \pv month BNB,BTC
    """
    available_commands = ('\\pv')
    is_command = any(command for command in available_commands if message.startswith(command))
    splitted = message.split()
    if is_command and len(splitted) == 3:
        if splitted[1] in ('month', 'week', 'year', '-m', '-w', '-y'):
            return True
    return False 

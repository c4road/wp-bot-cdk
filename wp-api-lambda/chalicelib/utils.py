def validate_command(message):
    """
    Validate a message is a command
    :params str message: the message body
    """
    available_commands = ['\\pv',]
    is_command = any(command for command in available_commands if message.statswith(command))
    if is_command and len(message.split()) == 3:
        return True
    return False 

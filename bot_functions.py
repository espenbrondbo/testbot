import weather

def is_channel(channel):
    """Return true if the variable is an IRC channel. False otherwise.

    Keyword argument:
    channel -- string
    """
    return channel.startswith('#')

def is_weather_command(message):
    """Check wether a message is a weather prompt or not.

    Keyword argument:
    message -- message received from a channel or from a user
    """
    return message.startswith('!weather')

def get_city_name_from_message(message):
    """Extract the city name from a received weather request

    Keyword argument:
    message -- message received from a channel or from a user
    """
    info = message.split(' ')
    if len(info) < 1:   # must be greater than 1 to include a city name
        return 'Could not find weather data.'
    else:
        try:
            data = weather.get_weather_string(info[1]) 
            return data
        except:
            return 'Invalid city name'

def is_leave_command(message):
    """check whether a message is a leave command or not.

    Keyword argument:
    message -- message received from a channel or a user
    """
    return message.startswith('!leave')

def is_status_command(message):
    """check whether a message is a leave command or not.

    Keyword argument:
    message -- message received from a channel or a user
    """
    return message.startswith('!status')

def is_join_command(message):
    """Check whether a message is a join command or not.

    Keyword argument:
    message -- message received from a channel or from a user
    """
    return message.startswith('!join')

def get_user_name_from_message(message):
    """Extract user name from a received message

    Keyword argument:
    message -- message reveiced from user or channel
    """
    return message.split('!')[0]

def get_channels_from_message(message):
    """Extract channels names from a received message

    Keyword argument:
    message -- message received  from a channel or from a user
    """
    info = message.split(' ')
    if len(info) > 1:
        return info[1:]
    return None

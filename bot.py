# twisted imports
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.python import log

# imports from the project 
import bot_functions
import url_functions

class TestBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
        log.msg('Signed on as {}.'.format(self.nickname))

    def joined(self, channel):
        log.msg('Joined {}.'.format(channel))

    def left(self, channel):
        log.msg('Left {}'.format(channel))

    def privmsg(self, user, channel, message):
        if bot_functions.is_weather_command(message):	# check if message is weather command
            log.msg('Weather request from {} in {}'.format(user, channel))
            self.handle_weather(user, channel, message)
        elif url_functions.contains_url(message):		# check if message contains URL
            log.msg('{} posted URL to {}'.format(user, channel))
            url = url_functions.get_url(message)
            title = url_functions.get_title(url)
            self.msg(channel, title)
        elif bot_functions.is_join_command(message):
            log.msg('Join request from {} in {}'.format(user, channel))
            self.handle_join(user, channel, message)
        elif bot_functions.is_leave_command(message):
            log.msg('Leave request from {} in {}'.format(user, channel))
            self.handle_leave(user, channel, message)
        elif bot_functions.is_status_command(message):
            log.msg('Status request from {} in {}'.format(user,channel))
            self.handle_status(user, channel, message)

    def handle_status(self, user, channel, message):
        if not bot_functions.is_channel(channel): # check if message was sent directly to the bot
            user_name = bot_functions.get_user_name_from_message(user)
            if user_name in self.factory.admins: # check if message was sent by admin
                log.msg(self.factory.channels)



    def handle_leave(self, user, channel, message):
        """Called when bot received a leave command. Leaves specified channels if message came directly from user and user is an admin.

        Keyword arguments:
        user -- user that sent message
        channel -- channel message is received from
        message -- message sent by user
        """
        if not bot_functions.is_channel(channel): # check if message was sent directly to the bot
            user_name = bot_functions.get_user_name_from_message(user)
            if user_name in self.factory.admins: # check if message was sent by admin
                channels = bot_functions.get_channels_from_message(message)
                for channel in channels:
                    self.leave(channel)
                    self.remove_channel(channel)

    def add_channel(self, channel):
        """Add a channel to channel list.

        Keyword argument:
        channel -- channel to add
        """
        if not channel.startswith('#'):
            channel = '#' + channel
        if channel not in self.factory.channels:
            self.factory.channels.append(channel)

    def remove_channel(self, channel):
        """Remove a channel from channel list.

        Keyword argument:
        channel -- channel to remove
        """
        if not channel.startswith('#'):
            channel = '#' + channel
        if channel in self.factory.channels:
            self.factory.channels.remove(channel)

    def handle_weather(self, user, channel, message):
        """Called when bot receives a weather command. Decide if reply should be to user or channel

        Keyword arguments:
        user -- user that sent message
        channel -- channel message is received from
        message -- message sent by user
        """
        return_message = bot_functions.get_city_name_from_message(message)
        if bot_functions.is_channel(channel):
            self.msg(channel, return_message)
        else:
            user_name = bot_functions.get_user_name_from_message(user)
            self.msg(user_name, return_message)

    def handle_join(self, user, channel, message):
        """Join channels specified in message if message is from an admin.

        Keyword arguments:
        user -- user that sent message
        channel -- channel message is received from
        message -- message sent by user 
        """
        if not bot_functions.is_channel(channel): # check if message was sent directly to the bot
            user_name = bot_functions.get_user_name_from_message(user)
            if user_name in self.factory.admins: # check if message was sent by admin
                channels = bot_functions.get_channels_from_message(message)
                for channel in channels:
                    self.join(channel)
                    self.add_channel(channel)


class TestBotFactory(protocol.ClientFactory):
    protocol = TestBot

    def __init__(self, channels, admins, nickname='thisisfun00', owner='whatiswronghere'):
        self.channels = channels
        self.nickname = nickname
        self.owner = owner
        self.admins = admins

    def clientConnectionLost(self, connector, reason):
        log.msg('Lost connection ({}), reconnecting'.format(reason))
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        log.msg('Could not connect: {}'.format(reason))

import sys
from twisted.internet import reactor
import config

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    reactor.connectTCP(config.bot['server'], config.bot['port'],
            TestBotFactory(config.bot['channels'], config.bot['admins'], nickname=config.bot['username']))
    reactor.run()

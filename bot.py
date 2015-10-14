# twisted imports
from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.python import log

# imports from the project 
import bot_functions

class TestBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        log.msg('Signed on as {}.'.format(self.nickname))

    def joined(self, channel):
        log.msg('Joined {}.'.format(channel))

    def privmsg(self, user, channel, message):
        log.msg(user, channel, message)
        if bot_functions.is_weather_command(message):
            return_message = bot_functions.get_city_name_from_message(message)
            if bot_functions.is_channel(channel):
                self.msg(channel, return_message)
            else:
                user_name = bot_functions.get_user_name_from_message(user)
                self.msg(user_name, return_message)


class TestBotFactory(protocol.ClientFactory):
    protocol = TestBot

    def __init__(self, channel, nickname='thisisfun00', owner='whatiswronghere'):
        self.channel = channel
        self.nickname = nickname
        self.owner = owner

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
            TestBotFactory(config.bot['channel']))
    reactor.run()

# Copyright © 2011, Kristofer Hallin (kristofer.hallin@gmail.com)
#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import os
import sys
import irclib
import module
import title

# The IRC bot itself
class Bot(object):

    # Set needed variables when created
    def __init__(self, nick, server, port, channel):
        self.nick = nick
        self.server = server 
        self.port = port
        self.channel = channel

        self.module = module.Module()
        self.title = title.Title()

    def on_connect(self, connection, event):
        return connection.join(self.channel)

    def on_disconnect(self, connection, event):
        return connection.connect(self.server, self.port, self.nick)

    # Event handler, all events will be parsed here
    def on_event(self, connection, event):        
        arg = event.arguments()[0]
        argp = arg.partition(' ')
        nickname = event.source().split('!')[0]

        # Allow empty arguments
        if len(argp[2]) == 0:
            argument = ""
        else:
            argument = argp[2]

        # Find out if this is a URL
        ret = self.title.parse_title(argp[0])
        if ret != None:
            return connection.privmsg(self.channel, ret)

        # Try to parse the event and execute from modules if available
        try:
            # If this fails, module.action_fallback will be called
            ret = self.module.actions.get(argp[0], 
                                          self.module.action_fallback)(nickname, argument)
        except:
            return connection.privmsg(self.channel, "Module threw exception")
        
        if ret != None:
            connection.privmsg(self.channel, ret)
            
    # Process IRC events
    def start(self):
        self.irc.process_forever()

    # Create IRC socket and register handlers
    def create(self):
        self.irc = irclib.IRC()
 
        connection = self.irc.server().connect(self.server, 
                                               self.port, 
                                               self.nick)

        connection.add_global_handler("welcome", self.on_connect)
        connection.add_global_handler("disconnect", self.on_disconnect)
        connection.add_global_handler("pubmsg", self.on_event)

        return connection

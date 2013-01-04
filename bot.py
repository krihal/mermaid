# Copyright 2011, Kristofer Hallin (kristofer.hallin@gmail.com)
#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import os
import sys
import log
import irclib
import module
import title

class Bot(object):
    def __init__(self, nick, server, port, channel):
        self.log = log.Logger("bot")
        self.nick = nick
        self.server = server 
        self.port = port
        self.channel = channel

        self.module = module.Module()
        self.title = title.Title()

    def on_connect(self, connection, event):
        self.log.debug("Connected, joining channel")
        return connection.join(self.channel)

    def on_disconnect(self, connection, event):
        self.log.debug("Disconnected")
        return connection.connect(self.server, self.port, self.nick)

    def on_event(self, connection, event):        
        self.log.debug("Got event, parsing")
        arg = event.arguments()[0]
        argp = arg.partition(' ')
        
        nickname = event.source().split('!')[0]

        if len(argp[2]) == 0:
            argument = ""
        else:
            argument = argp[2]

        ret = self.title.parse_title(argp[0])
        if ret != None:
            return connection.privmsg(self.channel, ret)

        try:
            ret = self.module.actions.get(argp[0], 
                                          self.module.action_fallback)(nickname, argument)
        except Exception as e:
            self.log.debug("Module " + argp[0] + " threw exception: %s\n" % (e))
            return connection.privmsg(self.channel, "Module threw exception")
        
        if ret != None:
            self.log.debug("To channel: " + ret)
            connection.privmsg(self.channel, ret)
            
    def start(self):
        self.irc.process_forever()

    def create(self):
        self.irc = irclib.IRC()

        self.log.debug("Connecting")
        connection = self.irc.server().connect(self.server, 
                                               self.port, 
                                               self.nick)
                       
        connection.add_global_handler("welcome", self.on_connect)
        connection.add_global_handler("disconnect", self.on_disconnect)
        connection.add_global_handler("pubmsg", self.on_event)

        return connection

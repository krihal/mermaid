#
# Copyright 2011, Kristofer Hallin (kristofer.hallin@gmail.com)
#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import socket
import select
import urlparse
import urllib
import os 
import sys
import ConfigParser

import bot
import log
import listener
import threading
from os.path import exists

# Fork to background
def daemonize():

    # Fork to background
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

# Create objects and sockets
def launch(nickname, server, port, channel, listenerport):

    # Create Bot instance
    mermaid = bot.Bot(nickname, server, port, channel)
    ircsocket = mermaid.create()

    # Create listener instance
    talker = listener.Listener(listenerport, ircsocket, channel)
    lsocket = talker.create()
    
    return talker, mermaid

# Create threads and start the bot
def create_threads(talker, mermaid):

    # Create listener thread
    listener_thread = threading.Thread(target = talker.start)

    # Creat bot thread
    bot_thread = threading.Thread(target = mermaid.start)

    # Start threads
    listener_thread.start() 
    bot_thread.start()

def main():

    # Configuration
    nickname = "MooPoo"
    server = "irc.freenode.org"
    port = 6667
    channel = "#flapflap"
    listenerport = 1234

#    daemonize()
    talker, mermaid = launch(nickname, server, port, channel, listenerport)
    create_threads(talker, mermaid)

if __name__ == '__main__':
    main()

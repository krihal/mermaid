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
import notifier
import threading
from os.path import exists

# Fork to background
def daemonize():

    # Fork to background
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

# Create objects and sockets
def launch(nickname, server, port, channel, listenerport, paths):

    # Create Bot instance
    mermaid = bot.Bot(nickname, server, port, channel)
    ircsocket = mermaid.create()

    # Create listener instance
    talker = listener.Listener(listenerport, ircsocket, channel)
    lsocket = talker.create()
    
    # Notify support
    notify = notifier.Notifier(ircsocket, channel, paths)    

    return talker, mermaid, notify

# Create threads and start the bot
def create_threads(talker, mermaid, notify):

    # Create listener thread
    listener_thread = threading.Thread(target = talker.start)

    # Creat bot thread
    bot_thread = threading.Thread(target = mermaid.start)

    # Notify thread
    notify_thread = threading.Thread(target = notify.start)

    # Start threads
    listener_thread.start() 
    bot_thread.start()
    notify_thread.start()

def main():

    # Configuration
    nickname = "XXX"
    server = "irc.quakenet.org"
    port = 6667
    channel = "XXX"
    listenerport = 1234
    paths = "XXX"

    daemonize()
    talker, mermaid, notify = launch(nickname, server, port, channel, listenerport, paths)
    create_threads(talker, mermaid, notify)

if __name__ == '__main__':
    main()

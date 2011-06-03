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

from bot import bot
from listener import listener
from threading import Thread
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
    mermaid = Bot(nickname, server, port, channel)
    ircsocket = mermaid.create()

    # Create listener instance
    talker = Listener(listenerport, ircsocket, channel)
    lsocket = talker.create()
    
    return talker, mermaid

# Create threads and start the bot
def create_threads(talker, mermaid):

    # Create listener thread
    listener_thread = Thread(target = talker.start)

    # Creat bot thread
    bot_thread = Thread(target = mermaid.start)

    # Start threads
    listener_thread.start() 
    bot_thread.start()

def main():

    # Configuration
    config = ConfigParser.RawConfigParser()
    config.read("mermaid.cfg")

    nickname = config.get("nickname", "bot")
    server = config.get("server", "bot")
    port = config.getint("port", "bot")
    channel = config.get("channel", "bot")
    listenerport = config.get("port", "listener")

    daemonize()
    talker, mermaid = launch(nickname, server, port, channel, listenerport)
    create_threads(talker, mermaid)

if __name__ == '__main__':
    main()

# Copyright 2011, Kristofer Hallin (kristofer.hallin@gmail.com)
#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import os
import sys
import log
import socket
import select

# Create a socket and send events to IRC channel
class Listener(object):

    # Set variables when created
    def __init__(self, port, ircsocket, ircchannel):
        self.log = log.Logger("listener")
        self.port = port
        self.ircsocket = ircsocket
        self.ircchannel = ircchannel

    def socket_create(self):
        self.log.debug("Created socket")
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_bind(self, serversocket):
        self.log.debug("Bound socket")
        serversocket.bind(("", 1234))

    def socket_listen(self, serversocket):
        serversocket.listen(5)
        self.serversocket = serversocket
        self.log.debug("Listening on socket")

    def socket_accept(self, serversocket):
        client, address = serversocket.accept()
        self.log.debug("Accepting connections")
        return client, address

    def socket_read(self, serversocket):
        self.log.debug("Received data on socket")
        return serversocket.recv(1024)

    def create(self):
        serversocket = self.socket_create()
        self.socket_bind(serversocket)
        self.socket_listen(serversocket)
        return serversocket

    # Start event loop
    def start(self):
        while 1:            
            listener = [self.serversocket]
            
            # Wait for something to arrive to socket
            self.log.debug("Waiting for data")                    
            ready = select.select(listener,[],[])
            if not ready:
                continue

            client, address = self.socket_accept(self.serversocket)
            data = self.socket_read(client)            
            if data:
                self.log.debug("Received data on socket")
        
                # Send read string to channel
                self.ircsocket.privmsg(self.ircchannel, data)
                client.close()

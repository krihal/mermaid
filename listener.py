# Copyright (C) 2011, Kristofer Hallin (kristofer.hallin@gmail.com)
#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import os
import sys
import socket
import select

# Create a socket and send events to IRC channel
class Listener(object):

    # Set variables when created
    def __init__(self, port, ircsocket, ircchannel):
        self.port = port
        self.ircsocket = ircsocket
        self.ircchannel = ircchannel

    def socket_create(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_bind(self, serversocket):
        serversocket.bind(("", 1234))

    def socket_listen(self, serversocket):
        serversocket.listen(5)
        self.serversocket = serversocket

    def socket_accept(self, serversocket):
        client, address = serversocket.accept()
        return client, address

    def socket_read(self, serversocket):
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
            ready = select.select(listener,[],[])
            if not ready:
                continue

            client, address = self.socket_accept(self.serversocket)
            data = self.socket_read(client)            
            if data:
                # Send read string to channel
                self.ircsocket.privmsg(self.ircchannel, data)
                client.close()

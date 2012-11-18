import os
import sys
import log
import socket
import select

#
# Network handling library
#
class NetLib(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create(self):
        res = socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC,
                                 socket.SOCK_STREAM, 0, socket.AI_PASSIVE)

        self.af, self.socktype, self.proto, self.canonname, self.sa = res[0]

        try:
            sock = socket.socket(socket.AF_INET, self.socktype, self.proto)
        except socket.error as msg:
            print "Failed to create socket: %s" % msg
            return -1

        return sock

    def close(self, sock):
        return sock.close()

    def connect(self, sock):
        try:
            res = sock.connect(self.sa)
        except socket.error as msg:
            print "Failed to connect socket: %s" % msg

        return res

    def send(self, sock, buffer):
        return sock.send(buffer)
        
    def read(self, sock):
        return sock.recv(128)

    def select(self, sock):
        ready = select.select([sock],[],[])
        if not ready:
            return False

        return True

    def bind(self, sock, port):
        try:
            res = sock.bind("", port)
        except socket.error as msg:
            print "Failed to bind socket: %s" % msg

    def listen(self, sock):
        return sock.listen(5)

    def accept(self, sock):
        conn, address = sock.accept()
        return conn, address

if __name__ == '__main__':
    n = NetLib("irc.quakenet.org", 6667)
    s = n.create()
    n.connect(s)
    if n.select(s):
        print n.read(s)
    n.close(s)

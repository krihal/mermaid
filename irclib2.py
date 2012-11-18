import re
import sys
import time
import signal
import network

#
# IRC library, implements NetLib
#
class IRCLib(network.NetLib):
    def __init__(self, host, port, nick):
        self.host = host
        self.port = port
        self.nick = nick
        self.channels = {}
        self.net = network.NetLib(self.host, self.port)
        self.sock = self.net.create()
         
    def __match_str__(self, str, pattern):
        match = re.match(pattern, str)
        if match:
            return match.group(0)
        
        return False
                    
    def __timeout__(self, signum, frame):
        raise Exception("Timeout")

    def connect(self):
        self.net.connect(self.sock)

        signal.signal(signal.SIGALRM, self.__timeout__)
        signal.alarm(30)
        
        try:
            while 1:
                if self.net.select(self.sock):                
                    buf = self.net.read(self.sock)
                    print buf
                if self.__match_str__(buf, ".+Checking Ident"):
                    self.net.send(self.sock, 
                                  "USER MyRealName * * :My Description\r\n")
                    self.net.send(self.sock, "NICK %s\r\n" % self.nick)
                    signal.alarm(30)
                if self.__match_str__(buf, ".+MODE.+:"):
                    break
        except Exception, e:
            print "Connection failed: %s" % e
            sys.exit()

        signal.alarm(0)
        return self

    def disconnect(self):
        return self.net.close(self.sock)

    def add_handler(self, handler, callback):
        return

    def __ping__(self, buf, sock):
        if self.__match_str__(buf, "PING :[0-9]+"):
            seq = buf.split(':')[1]
            self.net.send(sock, "PONG :%s" % seq)
            return True
        return False

    def join(self, channel):
        return self.net.send(self.sock, "JOIN %s" % channel)

    def privmsg(self, channel, msg):
        return self.net.send(self.sock, "PRIVMSG %s :%s\r\n" % (channel, msg))

    def process_forever(self):
        while 1:
            if self.net.select(self.sock):
                buf = self.net.read(self.sock)
            if self.__ping__(buf, sock):
                continue
            if __match_handlers__(buf, sock):
                continue
        return
#
# Tests
#
if __name__ == '__main__':
    def handler_connect(con):
        print "Connected!"
        
    def handler_disconnect(con):
        print "Disconnected!"

    def handler_join(con):
        print "Joined!"

    def handler_pubmsg(con, msg):
        print "Message: %s" % msg

    i = IRCLib("irc.freenode.org", 6667, "gnarpknark")
    con = i.connect()
    con.add_handler("connected", handler_connect)
    con.add_handler("connected", handler_disconnect)
    con.add_handler("connected", handler_join)
    con.add_handler("connected", handler_pubmsg)
    con.join("#testhest")
    con.privmsg("#testhest", "test")
    con.disconnect()

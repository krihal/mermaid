import os
import socket
import pyinotify

class EventException(Exception):
    pass

class Notify(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        raise EventException("Created: %s " % os.path.join(event.path, event.name))

class Notifier():
    def __init__(self, ircsocket, ircchannel, path):
        self.wm = pyinotify.WatchManager()
        self.mask = pyinotify.IN_CREATE
        self.notifier = pyinotify.Notifier(self.wm, Notify())
        self.wdd = self.wm.add_watch(path, self.mask, rec=True)
        self.ircsocket = ircsocket
        self.ircchannel = ircchannel

    def start(self):
        while True:
            try:
                a = self.notifier.process_events()
                if self.notifier.check_events():
                    self.notifier.read_events()
            except EventException, e:
                print e
                self.ircsocket.privmsg(self.ircchannel, e)
            except KeyboardInterrupt:
                self.notifier.stop()
                break

if __name__ == '__main__':
    n = Notifier(None, "/home/khn/tmp")
    n.start()

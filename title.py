# Copyright (C) 2011, Kristofer Hallin (kristofer.hallin@gmail.com)
#
# Mermaid, IRC bot written by Kristofer Hallin
# kristofer.hallin@gmail.com
#

import os
import re
import sys
import socket
import urllib2

class Title(object):
    def __init__(self):
        return

    def is_url(self, url):
        if not re.search('((https?:\/\/|www\.)\S+)', url, re.IGNORECASE):
            return None

        if not re.search('[^:]+:\/\/', url):
            url = 'http://' + url

        return url

    def extract_html(self, url):
        timeout_time = socket.getdefaulttimeout()
        socket.setdefaulttimeout(15)

        try:
            data = urllib2.urlopen(url)
        except:
            return None

        html = data.read();
        socket.setdefaulttimeout(timeout_time)       
        
        return html

    def get_title(self, html):
        m = re.search('<title[^>]*>\s*(.+?)\s*<\/title>', html, re.IGNORECASE|re.MULTILINE)
        if m:
            title = m.group(1)
            title = re.sub('\s+', ' ', title)
            return title

        return None


    def parse_title(self, url):
        url = self.is_url(url)
        if url == None:
            return None

        html = self.extract_html(url)
        if html == None:
            return None

        return self.get_title(html)

if __name__ == '__main__':
    title = Title()

    ret = title.parse_title("http://www.google.com")
    if ret != None:
        print ret

    ret = title.parse_title("www.youtube.com/watch?v=BcsduzIF2p0")
    if ret != None:
        print ret

    ret = title.parse_title("www.sadasdasdsssssss.com")
    if ret != None:
        print ret

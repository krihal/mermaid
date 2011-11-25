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
        data = urllib2.urlopen(url)
        html = data.read();
        socket.setdefaulttimeout(timeout_time)       
        
        return html

    def parse_title(self, url):
        url = self.is_url(url)
        if url == None:
            return      

        html = self.extract_html(url)
        m = re.search('<title[^>]*>\s*(.+?)\s*<\/title>', html, re.IGNORECASE|re.MULTILINE)
        if m:
            title = m.group(1)
            title = re.sub('\s+', ' ', title)
            return title

        return None

if __name__ == '__main__':
    title = Title()
    print title.parse_title("http://www.google.com")
    print title.parse_title("http://www.youtube.com")

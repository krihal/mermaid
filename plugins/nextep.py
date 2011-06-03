import re
import sys
import urlparse
import urllib
from os.path import exists

def fetch_show(nickname, show):
    info = {}
    match = re.compile(r"(.*?)@(.*)")

    url = "http://services.tvrage.com/tools/quickinfo.php?show=%s" % urllib.quote(show)
    f = urllib.urlopen(url)

    for line in f:
        m = match.search(line)
        if m != None:
            info[m.group(1)] = m.group(2)

    if "Show Name" in info:
        next_ep = "Not scheduled"
        prev_ep = "Unknown date"

        if "Next Episode" in info:
            next_ep = info["Next Episode"].replace("^", ", ")

        if "Latest Episode" in info:
            prev_ep = info["Latest Episode"].replace("^", ", ")

        return "Last episode: " + prev_ep + " Next episode: " + next_ep

    return "Next episode for " + show + " not found"

def __register__(actions):
    actions[".nextep"] = fetch_show

def __unregister__(actions):
    del actions[".nextep"]

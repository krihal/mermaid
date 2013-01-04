import sys
import socket
import urlparse
import urllib
import urllib2

def fetch_weather(nickname, city):

    if city.lower() == "my ass":
        return "Temperature in " + city + ": 37.7C, Humidity: 95%%, Wind: S at 40 mph"

    url = "http://www.google.com/ig/api?weather=" + urllib2.quote(city)

    try:
        f = urllib2.urlopen(url)
    except:
        return nickname + ": I could not find " + city

    s = f.read()

    weather = "Temperature in " + city + ": "
    weather += s.split("<temp_c data=\"")[-1].split("\"")[0]
    weather += "C, "
    weather += s.split("<humidity data=\"")[-1].split("\"")[0]
    weather += ", "
    weather += s.split("<wind_condition data=\"")[-1].split("\"")[0]
    weather += ", "
    weather += s.split("<condition data=\"")[1].split("\"")[0]

    if not "xml" in weather:
        return weather

    return nickname + ": I could not find " + city

def __register__(actions):
    actions[".weather"] = fetch_weather

def __unregister__(actions):
    del actions[".weather"]

if __name__ == "__main__":
	print fetch_weather("Hallin", "Stockholm")
	

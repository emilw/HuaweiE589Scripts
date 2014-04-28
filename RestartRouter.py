import requests
import xml.etree.ElementTree as ET
import sys
import datetime
import os
from twitter import *

_verbose = False
_routerIP = ''

def TwitterUpdate(message):
  CONSUMER_KEY = 'S4ef8eeTQanQyur3eSETPnM0Y'
  CONSUMER_SECRET = ''

  consumer_secret_path = os.path.expanduser('~/.twitter_homebot_consumersecret')

  with open (consumer_secret_path, "r") as myfile:
    CONSUMER_SECRET=myfile.read().replace('\n', '')

  MY_TWITTER_CREDS = os.path.expanduser('~/.twitter_homebot_oauth')
  if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("HomeBotApplication", CONSUMER_KEY, CONSUMER_SECRET,
                MY_TWITTER_CREDS)

  oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

  twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

  message = str(datetime.datetime.now()) + " - " + message
  # Now work with Twitter
  twitter.statuses.update(status=message)

def PrintDebugInfo(xmlTree, response, methodName):
  if(_verbose):
    print "Debug info(" + methodName + ")"
    if(response is not None):
      print "Response code from " + response.url + " was " + str(response.status_code)
      print "Response content: " + response.content

    if(xmlTree is not None):
      for child in xmlTree:
        print child.tag + ": " + child.text

    print "/End of Debug info(" + methodName + ")"

def Login(session):
  print "Logging in..."
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  xml = """<?xml version="1.0" encoding="UTF-8"?><request><Username>admin</Username><Password>YWRtaW4=</Password></request>"""
  r = s.post('http://' + _routerIP + '/api/user/login', data=xml, headers=headers, allow_redirects=True)

  tree = ET.fromstring(r.content)

  PrintDebugInfo(tree, r, "Login")
  print "Logged in"

def CheckLogin(session):
  print "Check if logged in..."
  r = s.get('http://' + _routerIP + '/api/user/state-login',timeout=1)

  tree = ET.fromstring(r.content)

  PrintDebugInfo(None, r, "CheckLogin")

  print tree[0].text
  if tree[0].text == '-1':
    print "Not logged in"
    return False
  else:
    print "Logged in"
    return True

def Restart(session):
  xml = """<?xml version="1.0" encoding="UTF-8"?><request><Control>1</Control></request>"""
  headers = {'Content-Type': 'application/xml'}
  r = s.post('http://' + _routerIP + '/api/device/control', data=xml, headers=headers, allow_redirects=True)
  tree = ET.fromstring(r.content)

  PrintDebugInfo(tree,r,"Restart")

  print "Router being restarted"

print datetime.datetime.now()

if(len(sys.argv) > 1):
  _routerIP = sys.argv[1]
  if(len(sys.argv) > 2 and sys.argv[2] == "--v"):
    _verbose = True
    print "Verbose mode is active"
else:
  print "Give IP number to the router as the first argument"
  sys.exit()

try:
  s = requests.Session()

  isLoggedIn = CheckLogin(s)

  if isLoggedIn == False:
    Login(s)

  if isLoggedIn or CheckLogin(s) == True:
    TwitterUpdate("Router is being restarted")
    Restart(s)
  else:
    print "Could not restart due to login problems, run with --v to get more information"

except Exception,e:
  print "Failed to connect to host"
  print e

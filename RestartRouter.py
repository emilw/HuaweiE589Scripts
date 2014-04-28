import requests
import xml.etree.ElementTree as ET
import sys

_verbose = False

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
  r = s.post('http://192.168.10.1/api/user/login', data=xml, headers=headers, allow_redirects=True)

  tree = ET.fromstring(r.content)

  PrintDebugInfo(tree, r, "Login")
  print "Logged in"

def CheckLogin(session):
  print "Check if logged in..."
  r = s.get('http://192.168.10.1/api/user/state-login',timeout=1)

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
  r = s.post('http://192.168.10.1/api/device/control', data=xml, headers=headers, allow_redirects=True)
  tree = ET.fromstring(r.content)

  PrintDebugInfo(tree,r,"Restart")

  print "Router being restarted"

if(len(sys.argv) > 1):
  if(sys.argv[1] == "--v"):
    _verbose = True
    print "Verbose mode is active"

try:
  s = requests.Session()

  isLoggedIn = CheckLogin(s)

  if isLoggedIn == False:
    Login(s)

  if isLoggedIn or CheckLogin(s) == True:
    Restart(s)
  else
    print "Could not restart due to login problems, run with --v to get more information"

except Exception,e:
  print "Failed to connect to host"
  print e

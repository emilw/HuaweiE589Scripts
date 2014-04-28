import requests
import xml.etree.ElementTree as ET

try:
  #r = requests.get('http://192.168.10.1/api/net/current-plmn', timeout=1)
  r = requests.get('http://192.168.10.1/api/monitoring/converged-status', timeout=1)

  if r and r.status_code == requests.codes.ok:
    print "A connection was made to " + r.url
    print "Processing result"
    tree = ET.fromstring(r.content);

    #print tree.find("WifiStatus").text

    #print "Raw content:"
    #print r.text
    #print tree.tag
    print "Wifi status:"
    for child in tree:
      print child.tag + ": " + child.text
    print "/End of Wifi status"
  else:
    print "Failed to connect"
except Exception,e:
  print "Failed to connect to host"
  print e

#print r.text.WifiStatus
print "End of program"

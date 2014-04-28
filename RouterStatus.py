import requests
import xml.etree.ElementTree as ET

try:
  r = requests.get('http://192.168.10.1/api/monitoring/status', timeout=1)
  r2 = requests.get('http://192.168.10.1/api/wlan/host-list',timeout=1)
  if r and r.status_code == requests.codes.ok:
    print "A connection was made to " + r.url
    print "Processing result"
    tree = ET.fromstring(r.content)
    tree2 = ET.fromstring(r2.content)

    #print tree.find("WifiStatus").text

    #print "Raw content:"
    #print r.text
    #print tree.tag
    print "Wifi status:"
    for child in tree:
      print child.tag + ": " + child.text
    print "/End of Wifi status"

    print "Hosts"
    tree2 = tree2[0]

    connectedHosts = 0

    for child in tree2:
      print "---------Host---------"
      for prop in child:
        print prop.tag + ":"
        if(prop.text is not None):
          print prop.text
      print "---------/Host---------"
      connectedHosts = connectedHosts + 1

    print "Number of hosts connected:"
    print connectedHosts

    print "/Hosts"

  else:
    print "Failed to connect"
except Exception,e:
  print "Failed to connect to host"
  print e

#print r.text.WifiStatus
print "End of program"

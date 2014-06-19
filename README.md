#Intro
I needed to remote control my Huawei E589 4G Wifi router. I did some reveresed engineering on the call from the web site and manage to package them in two python scripts. One that shows the current status of the router, e.g. connected clients, signal etc. and the other one restarts the router.

Example use cases is to schedule the restart script every night. I sometimes feel that the Wifi router starts to loose performance after 24 hours.

#Get started!

###Get all the packages

`$sudo apt-get install git`

`$sudo apt-get install ca-certicficates`

`$sudo apt-get install python-pip`

###Get the package manager for python(Pip)

`$sudo pip install requests`

###Get the scripts from github

`$git clone https://github.com/emilw/HuaweiE589Scripts.git`

###Run the python scripts
`cd HuaweiE589Scripts`
`$python RouterStatus.py 192.168.10.1`
or
`$python RestartRouter.py 192.168.10.1`

#!/usr/bin/env python
#Joshua Meyer
#5 June 2017

#Creates a batman mesh node

import __init__ as globalvars
import os
import sys
import apt

if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this script\n")

pkg_name = "batctl"
wlan = "wlan0"
cache = apt.cache.Cache
cache.update()

pkg = cache[pkg_name]
if pkg.is_installed:
    print "{pkg_name} already installed".format(pkg_name=pkg_name)
else:
    pkg.mark_install()

    try:
        cache.commit()
    except Exception, arg:
        print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))



#enable batman-adv module
os.system("modprobe batman-adv")


#configure network
os.system("sudo ifconfig {wlan0} mtu 1528".format(wlan0=wlan))
os.system("ifconfig {wlan0} down".format(wlan0=wlan))
os.system("iwconfig {wlan0} mode ad-hoc essid my-mesh-network channel 1".format(wlan0=wlan))
os.system("sudo batctl if add {wlan0}".format(wlan0=wlan))
os.system("ifconfig {wlan0} up".format(wlan0=wlan))
os.system("ifconfig bat0 up")

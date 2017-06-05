#!/usr/bin/env python
#Joshua Meyer
#5 June 2017

#Creates a batman mesh node

import __init__ as globalvars
import os
import sys
import apt

class batnode(object):

    def __init__(self):
        self.pkg_name = "batctl"
        self.wlan = "wlan0"
        self.essid = "bat-mesh-network"
        self.ap = "02:12:34:56:78:90"


    def batinstall(self):
        if not os.geteuid() == 0:
            sys.exit("\nOnly root can run this script\n")

        cache = apt.cache.Cache
        cache.update()
        pkg = cache[self.pkg_name]
        if pkg.is_installed:
            print "{pkg_name} already installed".format(pkg_name=self.pkg_name)
        else:
            pkg.mark_install()

            try:
                cache.commit()
            except Exception, arg:
                print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))


    def createbatnode(self):
        #enable batman-adv module
        os.system("modprobe batman-adv")

        #configure network
        os.system("sudo ifconfig {wlan0} mtu 1528".format(wlan0=self.wlan))
        os.system("ifconfig {wlan0} down".format(wlan0=self.wlan))
        os.system("iwconfig {wlan0} mode ad-hoc essid {essid} ap {ap} channel 1".format(wlan0=self.wlan, ap=self.ap, essid=self.essid))
        os.system("sudo batctl if add {wlan0}".format(wlan0=self.wlan))
        os.system("ifconfig {wlan0} up".format(wlan0=self.wlan))
        os.system("ifconfig bat0 up")

if __name__ == "__main__":
    newbat = batnode()
    batnode.batinstall()
    batnode.createbatnode()
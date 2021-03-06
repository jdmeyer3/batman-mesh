#!/usr/bin/env python
# Joshua Meyer
# 5 June 2017

# Creates a batman mesh node

import __init__ as globalvars
import os
import sys
import apt

class batgwnode(object):

    def __init__(self):
        self.pkg_name = "batctl"
        self.wlan = "wlan0"
        self.eth = "eth0"
        self.bridgeip = "192.168.2.1"
        self.essid = "my-mesh-network"
        self.ap = "02:12:34:56:78:90"

    def installbat(self):
        if not os.geteuid() == 0:
            sys.exit("\nOnly root can run this script\n")

        cache = apt.Cache()
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
    def installbat0(self):
        os.system("apt-get update")
        os.system("apt-get install batctl")


    def createbatgw(self):
        # enable batman-adv module
        os.system("modprobe batman-adv")


        # enable batman node
        # configure network
        os.system("sudo ifconfig {wlan0} mtu 1528".format(wlan0=self.wlan))
        os.system("ifconfig {wlan0} down".format(wlan0=self.wlan))
        os.wait(3)
        os.system("iwconfig {wlan0} mode ad-hoc essid {essid} ap {ap} channel 1".format(wlan0=self.wlan, ap=self.ap, essid=self.essid))
        os.system("sudo batctl if add {wlan0}".format(wlan0=self.wlan))
        os.system("ifconfig {wlan0} up".format(wlan0=self.wlan))
        os.system("ifconfig bat0 up")

        # creates mesh bridge to internet
        os.system("ip link add name mesh-bridge type bridge")
        os.system("ifconfig {eth0} down".format(eth0=self.eth))
        os.wait(3)
        os.system("ip link set dev {eth0} master mesh-bridge".format(eth0=self.eth))
        os.system("ip link set dev bat0 master mesh-bridge")
        os.system("ip link set up dev {eth0}".format(eth0=self.eth))
        os.system("ip link set up dev bat0")
        os.system("ip link set up dev mesh-bridge")
        os.system("ifconfig mesh-bridge {ipaddr}".format(ipaddr=self.bridgeip))
        
if __name__ == "__main__":
    batgw = batgwnode()
    batgw.installbat0()
    batgw.createbatgw()
  
    

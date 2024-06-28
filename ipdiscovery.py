import subprocess
import os
from urllib.request import urlopen
import re as r
import socket


def self_ip():
    """
    Provides hostname, public and private IP information for current host.
    """
    # Finds hostname
    hostname = subprocess.check_output("hostname").decode("utf-8").strip()
    print("Hostname: " + hostname)

    # Finds IP address on current network
    privateIP = socket.gethostbyname(hostname)
    print("Private IP: " + privateIP)

    # Finds public IP of router 
    d = str(urlopen('http://checkip.dyndns.com/').read())
    publicIP = r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
    print("Public IP: " + publicIP)

def ip_discovery():
    """
    Gets a list of all IP addresses on the network using the arp command.

    """
    output = subprocess.check_output(("arp", "-a")).decode("utf-8").strip()
    # todo: filter command output to match only the addresses corresponding to your own interface
    # (my VMWare adapters are showing up individually)
    # strip everything that comes from a separate interface
    print(output)

self_ip()
ip_discovery()

import subprocess
import os
from urllib.request import urlopen
import re as r
import socket, struct

# Windows only!!!!!

class ip:
    # Gets hostname and private IP values to be shared across classes
    hostname = subprocess.check_output("hostname").decode("utf-8").strip()
    privateIP = socket.gethostbyname(hostname)

    def print_self_ip():
        """
        Provides hostname, public and private IP information for current host.
        """
    # Finds hostname
        print("Hostname: " + ip.hostname)

    # Finds IP address on current network
        print("Private IP: " + ip.privateIP)

    # Finds public IP of router 
        d = str(urlopen('http://checkip.dyndns.com/').read())
        publicIP = r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
        print("Public IP: " + publicIP)

    def ip_discovery():
        """
        Gets a list of all IP addresses on the network using the arp command.
        Reformats the list to include a list of IPs, corresponding MAC address, and hostname.
        """

    # Declares empty lists to store data
        ip_list = []
        mac_list = []
        hostname_list = []

    # Runs arp -a to get initial output, converts to string
        output = subprocess.check_output(("arp", "-a")).decode("utf-8").strip()

    # Finds index of the first appearance of private IP address
        outIndex = output.find(ip.privateIP)

    # Strips output, creates new list strippedOutput with data from arp command
        strippedOutput = output[outIndex:-1].splitlines()

    # Deletes section of ARP output w/ interface and item headers.
        del strippedOutput[0]
        del strippedOutput[0]
        ipaddr = ''
        mac = ''
        name = ''
        # 
        for i in strippedOutput:
            # removes "dynamic/static" designators (each at index 46 of ARP table), converts to uppercase
            i = i[:46].upper()
            # splits list in half, gets two variables (one representing IP, one representing MAC). sends to lists
            ipaddr = i[:23].strip()
            ip_list.append(ipaddr)
            mac = i[24:45].strip()
            mac_list.append(mac)

            # does nslookup on name
            # have to add try/catch blocks for "host not found"
            # only interested in middle value of tuple, will have to trim further
            name = socket.gethostbyaddr(ipaddr)
            print(name)


    # Return some kind of table (?)


if __name__ == "__main__":
    ip.ip_discovery()

import subprocess
import os
from urllib.request import urlopen
import re as r
import socket, struct

# Windows only!!!!!

class ip:
    # Gets hostname and private IP values to be shared across functions
    hostname = subprocess.check_output("hostname").decode("utf-8").strip()
    privateIP = socket.gethostbyname(hostname)

    # empty lists initialized to hold IP/MAC/hostname information
    ip_list = []
    mac_list = []
    hostname_list = []

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
        Returns three separate lists, one of IP addresses, one of MAC addresses, and one of hostnames.
        """

    # Declares empty lists to store data
        iplist = ip.ip_list
        maclist = ip.mac_list
        hostnamelist = ip.hostname_list
    
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
            iplist.append(ipaddr)
            mac = i[24:45].strip()
            maclist.append(mac)

            # does nslookup on name
            try: 
                # returns first value in the name tuple, the hostname itself
                name = list(socket.gethostbyaddr(ipaddr)).pop(0)
                hostnamelist.append(name)
            # handles "host not found" error by removing current IP/MAC entries
            except socket.herror:           
                iplist.remove(ipaddr)
                maclist.remove(mac)
                pass

    def print_lists():
        """
        Just prints out content of lists.
        """
        ip.ip_discovery()
        print(ip.ip_list)
        print(ip.mac_list)
        print(ip.hostname_list)

    def format_lists():
        """
        Convert lists to a table.
        """

if __name__ == "__main__":
    ip.print_lists()

import subprocess
from urllib.request import urlopen
import re as r
import socket

"""
Expanded (and needlessly complex) arp command, listing hostnames as well as IP + MAC addresses of the devices on the arp table.
Finished 7/2/24
"""

class ip:
    # Gets hostname and private IP values to be shared across functions
    hostname = subprocess.check_output("hostname").decode("utf-8").strip()
    privateIP = socket.gethostbyname(hostname)

    # empty lists initialized to hold IP/MAC/hostname information
    ip_list = []
    mac_list = []
    hostname_list = []

    def ip_discovery():
        """
        Gets a list of all IP addresses in arp table.
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

    def format_lists():
        """
        Convert lists to a table similar to output of the arp command, and outputs it.
        """
        ip.ip_discovery()
        
        # finds max length of each entry in the list for formatting the table
        max_ip_length = max(len(ip) for ip in ip.ip_list + ["Internet Address"])
        max_mac_length = max(len(mac) for mac in ip.mac_list + ["Physical Address"])
        max_hostname_length = max(len(host) for host in ip.hostname_list + ["Hostname"])

        # prepares to format strings based on max length
        format_string = f"{{:<{max_ip_length}}}  {{:<{max_mac_length}}}  {{:<{max_hostname_length}}}"
        
        # prints header
        header = format_string.format("Internet Address", "Physical Address", "Hostname")
        print(header)

        # and here's the list!
        length = len(ip.hostname_list)
        for i in range(length):
            print(format_string.format(ip.ip_list[i], ip.mac_list[i], ip.hostname_list[i]))

        
if __name__ == "__main__":
    ip.format_lists()

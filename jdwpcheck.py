#! /usr/bin/python3
# _*_ coding:utf-8 _*_

import socket
import ipaddress
from multiprocessing import Pool,Manager


def getTargets():
    target = open("test.txt",'r')
    cidr = target.readlines()
    return cidr

def generate_ip_addresses(cidr_list):
    ip_addresses = []
    for cidr in cidr_list:
        try:
            cidr = cidr.replace('\n','')
            network = ipaddress.ip_network(cidr, strict=False)
            ip_addresses.extend([str(ip) for ip in network])
        except ValueError as e:
            print("cidr converting error"+e)
        
    return ip_addresses

def saveinfo(result):
    if result:
        fw = open('jdwp_result','a')
        fw.write(result+'\n')
        fw.close()


def jdwpCheck1(target, q):
    print("checking target:"+target+":8000")
    socket.setdefaulttimeout(2)
    client = socket.socket()
    client.connect((target,8000))
    if client.recv(14) == b'JDWP-Handshake':
        print(target+":8000 jdwp found!")
        saveinfo(target+":8000 jdwp found!")
    
    client.close()


def jdwpCheck2(target, q):
    print("checking target:"+target+":8080")
    socket.setdefaulttimeout(2)
    client = socket.socket()
    client.connect((target,8080))
    if client.recv(14) == b'JDWP-Handshake':
        print(target+":8080 jdwp found!")
        saveinfo(target+":8080 jdwp found!")
    
    client.close()



def poolmana(ips):
    p = pool(60)
    q = Manager().Queue()
    for i in ips:
        i = i.replace('\n','')
        p.apply_async(jdwpCheck1, args=(i,q))
        p.apply_async(jdwpCheck2, args=(i,q))
    p.close()
    p.join()
    print("check complete,check jdwp_result.txt in current folder")

def run():
    targets = getTargets()
    ips = generate_ip_addresses(targets)
    poolmana(ips)

if __name__ == '__main__':
    run()

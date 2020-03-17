import netifaces

interfaces = netifaces.interfaces()
for i in interfaces:
    if i == 'lo':
        continue
    iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
    if iface != None:
        for my_j in iface:
           # print (my_j['addr'])
           pass

iface = netifaces.ifaddresses('eth1').get(netifaces.AF_INET)
print(iface[0]["addr"])

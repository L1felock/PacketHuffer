import json
import subprocess


#!/usr/bin/env python
print "Content-Type: text/html"
print

output = subprocess.check_output("ipconfig")
networkInterfaces = dict()
newInterface = 1
count = 0

for row in output.split('\n'):
    if ':' in row and ': ' not in row:
        key, value = row.split(':')
        networkInterfaces[count] = dict()
        networkInterfaces[count]['interface'] = key

        count += 1

count = -1

for row in output.split('\n'):
    if ':' in row and ': ' not in row:
        interface = row.strip()
        newInterface = 1
        count += 1
    else:
        newInterface = 0
    if ': ' in row and 'IPv4' in row:
        key, value = row.split(': ')
        networkInterfaces[count]['ip'] = value.strip()


length = len(networkInterfaces)
print "["
for i in networkInterfaces:

    temp = networkInterfaces[i]
    print json.dumps(temp, ensure_ascii=False)
    tempCount = i+1
    if length != tempCount:
        print ','
print "]"


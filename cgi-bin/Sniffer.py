__author__ = 'Colin'
from socket import *
import struct
import sys




print "Content-Type: text/html"
print

HOST = gethostbyname(gethostname())


s = socket(AF_INET, SOCK_RAW, IPPROTO_IP)
s.bind((HOST, 3001))




s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
s.ioctl(SIO_RCVALL, RCVALL_ON)
data = ''
try:
    data = s.recvfrom(65565)
except timeout:
    data = ''
except:
    print "An error happened: "#
    sys.exc_info() #
data = data[0]
print data[:20]

print

HeaderData = struct.unpack('!BBHiBBH4s4s' , data[:20])

print HeaderData

IpVersion = HeaderData[0] >> 4
print "IP Version: " + str(IpVersion)
HeadLength = HeaderData[0] & 15
print "Header Length: " + str(HeadLength * 4)

TotalLength = HeaderData[2]
print "Total Length: " + str(TotalLength)


if HeaderData[5] == 6:
    print "Protocol: TCP"
elif HeaderData[5] == 17:
    print "Protocol: UDP"
elif HeaderData[5] == 1:
    print "Protocol: ICMP"
else:
    print "Protocol: Other"



SourceIp = inet_ntoa(HeaderData[7])
print "Source IP: " + SourceIp
DestIp = inet_ntoa(HeaderData[8])
print "Destination IP: " + DestIp

print "Payload" + data[20:]


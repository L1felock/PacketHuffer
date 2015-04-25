__author__ = 'Colin'
from socket import *
import struct
import sys




print "Content-Type: text/html"
print

x = 1
while x < 20:
    x+=1
    HOST = gethostbyname(gethostname())


    s = socket( AF_PACKET , SOCK_RAW , ntohs(0x0003))

    data = ''
    try:
        data = s.recvfrom(65565)
    except timeout:
        data = ''
    except:
        print "An error happened: "#
        sys.exc_info() #
    data = data[0]

    print


    #Ethernet Header
    EthoData = struct.unpack('!cccccccccccc' , data[:12])

    print "Destination Address: " + str(EthoData[0].encode("hex")) + ":"+ str(EthoData[1].encode("hex")) + ":"+ str(EthoData[2].encode("hex")) + ":"+ str(EthoData[3].encode("hex")) + ":"+ str(EthoData[4].encode("hex")) + ":"+ str(EthoData[5].encode("hex"))
    print "Source Address: " + str(EthoData[6].encode("hex")) + ":"+ str(EthoData[7].encode("hex")) + ":"+ str(EthoData[8].encode("hex")) + ":"+ str(EthoData[9].encode("hex")) + ":"+ str(EthoData[10].encode("hex")) + ":"+ str(EthoData[11].encode("hex"))


    #IP Header
    HeaderData = struct.unpack('!BBHiBBH4s4s' , data[14:34])

    IpVersion = HeaderData[0] >> 4
    print "IP Version: " + str(IpVersion)
    HeadLength = HeaderData[0] & 15
    print "Header Length: " + str(HeadLength * 4)

    TotalLength = HeaderData[2]
    print "Total Length: " + str(TotalLength)
    print "Time To Live: " + str(HeaderData[4])
    SourceIp = inet_ntoa(HeaderData[7])
    print "Source IP: " + SourceIp
    DestIp = inet_ntoa(HeaderData[8])
    print "Destination IP: " + DestIp

    if HeaderData[5] == 6:
        print "Protocol: TCP"
        FooterData = struct.unpack('!HHLLHHi' , data[34:54])
        print "Source Port: " + str(FooterData[0])
        print "Destination Port: " + str(FooterData[1])
        print "Sequence Number: " + str(FooterData[2])
        print "Acknowledge Number: " + str(FooterData[3])
        print "Window Size: " + str(FooterData[5])
        print "Payload" + data[54:]


    elif HeaderData[5] == 17:
        print "Protocol: UDP"
        FooterData = struct.unpack('!HHHH' , data[34:42])
        print "Source Port: " + str(FooterData[0])
        print "Destination Port: " + str(FooterData[1])
        print "Length: " + str(FooterData[2])
        print "Payload" + data[42:]

    elif HeaderData[5] == 1:
        print "Protocol: ICMP"
        print "Payload: " + data[34:]
    else:
        print "Protocol: Other"
        print "Payload: " + data[34:]








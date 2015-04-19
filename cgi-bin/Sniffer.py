import json
from socket import *
import struct
import sys
import cgi, cgitb

get = cgi.FieldStorage()
interface = get.getvalue('interface')


fp = open("log.json", "w")

fpread = open("cgi-bin\\controller.txt", "r")
stopValue = fpread.read()
fpread.close()
fp.write("[")


packetCount = 0


while 1:
    #HOST = gethostbyname(gethostname())
    HOST = interface


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


    #IP Header
    HeaderData = struct.unpack('!BBHiBBH4s4s', data[:20])

    sniffedData = dict()

    IpVersion = HeaderData[0] >> 4
    #print "IP Version: " + str(IpVersion)
    sniffedData["IPVersion"] = str(IpVersion)
    HeadLength = HeaderData[0] & 15
    #print "Header Length: " + str(HeadLength * 4)

    TotalLength = HeaderData[2]
    #print "Total Length: " + str(TotalLength)
    sniffedData["TotalLength"] =  str(TotalLength)
    #print "Time To Live: " + str(HeaderData[4])
    sniffedData["TTL"] = str(HeaderData[4])
    SourceIp = inet_ntoa(HeaderData[7])
    #print "Source IP: " + SourceIp
    sniffedData["SourceIP"] = SourceIp
    DestIp = inet_ntoa(HeaderData[8])
    #print "Destination IP: " + DestIp
    sniffedData["DestinationIP"] = DestIp

    if HeaderData[5] == 6:
        #print "Protocol: TCP"
        sniffedData["Protocol"] = "TCP"
        FooterData = struct.unpack('!HHLLHHi' , data[20:40])
        #print "Source Port: " + str(FooterData[0])
        #print "Destination Port: " + str(FooterData[1])
        #print "Sequence Number: " + str(FooterData[2])
        #print "Acknowledge Number: " + str(FooterData[3])
        #print "Window Size: " + str(FooterData[5])
        #print "Payload" + data[40:]
        sniffedData["SourcePort"] = str(FooterData[0])
        sniffedData["DestinationPort"] = str(FooterData[1])
        sniffedData["SequenceNumber"] = str(FooterData[2])
        sniffedData["AcknowledgeNumber"] = str(FooterData[3])
        sniffedData["WindowSize"] = str(FooterData[5])
        sniffedData["Payload"] = data[40:]

    elif HeaderData[5] == 17:
        #print "Protocol: UDP"
        sniffedData["Protocol"] = "UDP"
        FooterData = struct.unpack('!HHHH' , data[20:28])
        #print "Source Port: " + str(FooterData[0])
        #print "Destination Port: " + str(FooterData[1])
        #print "Length: " + str(FooterData[2])
        #print "Payload" + data[28:]
        sniffedData["SourcePort"] = str(FooterData[0])
        sniffedData["DestinationPort"] = str(FooterData[1])
        #sniffedData["TotalLength"] = str(FooterData[2])
        sniffedData["Payload"] = data[28:]

    elif HeaderData[5] == 1:
        #print "Protocol: ICMP"
        #print "Payload: " + data[28:]
        sniffedData["Protocol"] = "ICMP"
        sniffedData["Payload"] = data[28:]

    else:
        #print "Protocol: Other"
        #print "Payload: " + data[20:]
        sniffedData["Protocol"] = "MISC"
        sniffedData["Payload"] = data[20:]

    sniffedData["ID"] = packetCount
    fp.write(json.dumps(sniffedData, ensure_ascii=False))

    fpread = open("cgi-bin\\controller.txt", "r")
    stopValue = fpread.read()
    fpread.close()
    if stopValue == 'stop':
        print "STOPPED"
        break
    else:
        fp.write(",")
    packetCount += 1


fp.write("]")

fpread.close()
fp.close()

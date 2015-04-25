import json
from socket import *
import struct
import sys
import cgi, cgitb

import math

#variables used to compute network diameter
averageDiameter = 0
diameterTally = 0
diameterCount = 0

get = cgi.FieldStorage()
interface = get.getvalue('interface')


fp = open("data//log.json", "w")
packetAveragesFP = open("data//packetAverages.json", "w")
congestionFP = open("data//congestionWindow.json", "w")
congestionWindowDict = dict()
congestionWindowDict["cols"] = [{"id":"task","type":"string"},{"id":"congestionwindow","label":"Congestion Window","type":"number"}]
congestionWindowDict["legend"] = {"position":"none"}
congestionWindowDict["rows"] = list()

packetAveragesDict = dict()

fpread = open("cgi-bin\\controller.txt", "r")
stopValue = fpread.read()
fpread.close()
fp.write("[")


packetCount = 1
totalPacketLength = 0

while 1:
    #HOST = gethostbyname(gethostname())
    HOST = interface


    s = socket(AF_INET, SOCK_RAW, IPPROTO_IP)
    #s.bind((HOST, 0))
    s.bind((HOST, 0))




    s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
    s.ioctl(SIO_RCVALL, RCVALL_ON)
    data = ''
    try:
        data = s.recvfrom(65565)
    except timeout:
        data = ''
    except:
        print "Error "#
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
    totalPacketLength += TotalLength

    sniffedData["TotalLength"] =  str(TotalLength)
    #print "Time To Live: " + str(HeaderData[4])
    sniffedData["TTL"] = str(HeaderData[4])

    #network diameter calculations
    if sniffedData["TTL"] < 128:
        diameterCount = diameterCount + 1
        diameterTally = diameterTally + math.abs(128-HeaderData[4])

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

        # SET HTTP PROTOCOL
        if str(FooterData[0]) == "80" or str(FooterData[1]) == "80":
            sniffedData["Protocol"] = "HTTP"
        sniffedData["SourcePort"] = str(FooterData[0])
        sniffedData["DestinationPort"] = str(FooterData[1])
        sniffedData["SequenceNumber"] = str(FooterData[2])
        sniffedData["AcknowledgeNumber"] = str(FooterData[3])
        sniffedData["WindowSize"] = str(FooterData[5])
        sniffedData["Payload"] = data[40:]

        # Congestion window stuff
        congestionWindowDict["rows"].append({"c":[{"v":packetCount},{"v": str(FooterData[5])}]})

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

    elif HeaderData[5] == 58:
        #print "Protocol: ICMPv6"
        #print "Payload: " + data[28:]
        sniffedData["Protocol"] = "ICMPv6"
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
        z = open("averageDiameter.txt", "w")
        if diameterCount > 0:
            averageDiameter = diameterTally/diameterCount
            z.write(str(averageDiameter))
        z.close()
        break
    else:
        fp.write(",")
    packetCount += 1


packetAveragesDict["totalLength"] = totalPacketLength
packetAveragesDict["numPackets"] = packetCount

congestionFP.write(json.dumps(congestionWindowDict, ensure_ascii=False))
packetAveragesFP.write(json.dumps(packetAveragesDict, ensure_ascii=False))

fp.write("]")
congestionFP.close()
fpread.close()
fp.close()
packetAveragesFP.close()

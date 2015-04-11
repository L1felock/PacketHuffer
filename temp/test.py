from socket import *
import struct
import sys
import re

# receive a datagram
def receiveData(s):
    data = ''
    try:
        data = s.recvfrom(65565)
    except timeout:
        data = ''
    except:
        print "An error happened: "
        sys.exc_info()
    return data[0]

# get Type of Service: 8 bits
def getTOS(data):
    precedence = {0: "Routine", 1: "Priority", 2: "Immediate", 3: "Flash", 4: "Flash override", 5: "CRITIC/ECP",
                  6: "Internetwork control", 7: "Network control"}
    delay = {0: "Normal delay", 1: "Low delay"}
    throughput = {0: "Normal throughput", 1: "High throughput"}
    reliability = {0: "Normal reliability", 1: "High reliability"}
    cost = {0: "Normal monetary cost", 1: "Minimize monetary cost"}

#   get the 3rd bit and shift right
    D = data & 0x10
    D >>= 4
#   get the 4th bit and shift right
    T = data & 0x8
    T >>= 3
#   get the 5th bit and shift right
    R = data & 0x4
    R = data & 0x4
    R >>= 2
#   get the 6th bit and shift right
    M = data & 0x2
    M >>= 1
#   the 7th bit is empty and shouldn't be analyzed

    tabs = '\n\t\t\t'
    TOS = precedence[data >> 5] + tabs + delay[D] + tabs + throughput[T] + tabs + \
            reliability[R] + tabs + cost[M]
    return TOS

# get Flags: 3 bits
def getFlags(data):
    flagR = {0: "0 - Reserved bit"}
    flagDF = {0: "0 - Fragment if necessary", 1: "1 - Do not fragment"}
    flagMF = {0: "0 - Last fragment", 1: "1 - More fragments"}

#   get the 1st bit and shift right
    R = data & 0x8000
    R >>= 15
#   get the 2nd bit and shift right
    DF = data & 0x4000
    DF >>= 14
#   get the 3rd bit and shift right
    MF = data & 0x2000
    MF >>= 13

    tabs = '\n\t\t\t'
    flags = flagR[R] + tabs + flagDF[DF] + tabs + flagMF[MF]
    return flags

# get protocol: 8 bits
def getProtocol(protocolNr):
    protocolFile = open('Protocol.txt', 'r')
    protocolData = protocolFile.read()
    protocol = re.findall(r'\n' + str(protocolNr) + ' (?:.)+\n', protocolData)
    if protocol:
        protocol = protocol[0]
        protocol = protocol.replace("\n", "")
        protocol = protocol.replace(str(protocolNr), "")
        protocol = protocol.lstrip()
        return protocol

    else:
        return 'No such protocol.'

# the public network interface
HOST = gethostbyname(gethostname())

# create a raw socket and bind it to the public interface
s = socket(AF_INET, SOCK_RAW, IPPROTO_IP)
s.bind((HOST, 3000))

# open file
fp = open("log.txt", "w")

while (1):

    # Include IP headers
    s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
    s.ioctl(SIO_RCVALL, RCVALL_ON)
    data = receiveData(s)

    # get the IP header (the first 20 bytes) and unpack them
    # B - unsigned char (1)
    # H - unsigned short (2)
    # s - string
    unpackedData = struct.unpack('!BBHHHBBH4s4s' , data[:20])

    version_IHL = unpackedData[0]
    version = version_IHL >> 4                  # version of the IP
    IHL = version_IHL & 0xF                     # internet header length
    TOS = unpackedData[1]                       # type of service
    totalLength = unpackedData[2]
    ID = unpackedData[3]                        # identification
    flags = unpackedData[4]
    fragmentOffset = unpackedData[4] & 0x1FFF
    TTL = unpackedData[5]                       # time to live
    protocolNr = unpackedData[6]
    checksum = unpackedData[7]
    sourceAddress = inet_ntoa(unpackedData[8])
    destinationAddress = inet_ntoa(unpackedData[9])

    # write to file

    fp.write("An IP packet with the size %i was captured.\n" % (unpackedData[2]))
    #print "An IP packet with the size %i was captured." % (unpackedData[2])
    fp.write("Raw data: " + data + "\n")
    #print "Raw data: " + data
    fp.write("\nParsed data\n")
    #print "\nParsed data"
    fp.write("Version:\t\t" + str(version) + "\n")
    #print "Version:\t\t" + str(version)
    fp.write("Header Length:\t\t" + str(IHL*4) + " bytes")
    #print "Header Length:\t\t" + str(IHL*4) + " bytes"
    fp.write("Type of Service:\t" + getTOS(TOS))
    #print "Type of Service:\t" + getTOS(TOS)
    fp.write("Length:\t\t\t" + str(totalLength))
    #print "Length:\t\t\t" + str(totalLength)
    fp.write("ID:\t\t\t" + str(hex(ID)) + " (" + str(ID) + ")")
    #print "ID:\t\t\t" + str(hex(ID)) + " (" + str(ID) + ")"
    fp.write("Flags:\t\t\t" + getFlags(flags))
    #print "Flags:\t\t\t" + getFlags(flags)
    fp.write("Fragment offset:\t" + str(fragmentOffset))
    #print "Fragment offset:\t" + str(fragmentOffset)
    fp.write("TTL:\t\t\t" + str(TTL))
    #print "TTL:\t\t\t" + str(TTL)
    fp.write("Protocol:\t\t" + getProtocol(protocolNr))
    #print "Protocol:\t\t" + getProtocol(protocolNr)
    fp.write("Checksum:\t\t" + str(checksum))
    #print "Checksum:\t\t" + str(checksum)
    fp.write("Source:\t\t\t" + sourceAddress)
    #print "Source:\t\t\t" + sourceAddress
    fp.write("Destination:\t\t" + destinationAddress)
    #print "Destination:\t\t" + destinationAddress
    fp.write("Payload:\n" + data[20:])
    #print "Payload:\n" + data[20:]
    fp.write("\n==============================================================\n")
# disabled promiscuous mode
s.ioctl(SIO_RCVALL, RCVALL_OFF)

# close file pointer
fp.close()
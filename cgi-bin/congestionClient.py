import json
from socket import *
import struct
import sys
import cgi, cgitb

PORT = 3004
COUNT = 50  # number of packets that will be sent
HOST = "dsh-s1.info"  # this is our remote server that you will bounce packets off of
BUFFERSIZE = 1024




def cwnd():
	congestionDict["cols"] = [{"id":"task","type":"string"},{"id":"wndsize", "label":"window size", "type":"number"}]
	congestionDict["legend"] = {"position":"none"}
	packetData = '1' * (BUFFERSIZE - 2) + '\n'
	
	s = socket(AF_INET, SOCK_RAW, IPPROTO_IP)
	s.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

	try:
        	s.connect((HOST, PORT))
    	except Exception, e:
        	print "could not connect"
	

	
	i = 0
	while i < COUNT:
		data = None
		s.send(packetData)
		while 1:
			data = conn.recv(BUFFERSIZE) #might need to put this in the other script
			if not data:
				break
		footerData = struct.unpack('!HHLLHHi' , data[20:40])
		cwnd = str(footerData[5])
		congestionDict["rows"].append({"c":[{"v":i},{"v":cwnd}]})
		i = i + 1

	outfile = open("congestionOutput.json", "w")
	outfile.write(json.dumps(congestionDict))


def main():
	while(1):
		f = open("cwndController.txt", "r")
		status = f.read().strip() #start and stop for going and stopping controlled by the interface
		f.close()
		if status == "start":
		    cwnd()

if __name__ == "__main__":
	main()

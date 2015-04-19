import time
import sys
import socket


PORT = 3002 #host and client will use the same port
BUFFERSIZE = 1024	
COUNT = 50  #number of packets that will be sent
HOST = "dsh-s1.info" #this is our remote server that you will bounce packets off of

def throughput():
	packetData = '1' * (BUFFERSIZE-2) + '\n'
	RTTList = list()
	averageThroughput = 0
	s = socket(AF_INET, SOCK_STREAM)

	try:
		s.connect((HOST,PORT))
	except Exception, e:
		print "could not connect"

	totalT1 = time.time()
	i = 0
	while i < count:
		t1 = time.time()
		s.sendall(packetData)
		t2 = time.time()
		RTTList.append(t2 - t1)
		i = i + 1
	totalT2 = time.time()
	averageThroughput = (BUFFERSIZE*COUNT*.0001)/(totalT2 - totalT1) #in mb/s
	totalTime = totalT2-totalT1 #in seconds



def main():
	while(1):
		f = open("throughputController.txt", "r")
		status = f.read().strip()
		if status == "start":
			throughput()
		else:
			continue


if __name___ == "__main__"
	main()
	


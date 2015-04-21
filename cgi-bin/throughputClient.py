from socket import *
import json, time, sys


PORT = 3003  # host and client will use the same port
BUFFERSIZE = 1024
COUNT = 500  # number of packets that will be sent
HOST = "dsh-s1.info"  # this is our remote server that you will bounce packets off of


def throughput():
    print "capturing throughput\n"

    packetData = '1' * (BUFFERSIZE - 2) + '\n'
    RTTList = list()
    averageThroughput = 0
    s = socket(AF_INET, SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
    except Exception, e:
        print "could not connect"

    totalT1 = time.time()

    i = 0
    while i < COUNT:
        t1 = time.time()
        s.send(packetData)
        t2 = time.time()
        RTTList.append(t2 - t1)
        i = i + 1
    totalT2 = time.time()
    averageThroughput = (BUFFERSIZE * COUNT * .0001) / (totalT2 - totalT1)  # in mb/s
    totalTime = totalT2 - totalT1  # in seconds

    outfile = open("cgi-bin\\throughputOutput.txt", "w")

    i = 1
    throughputDict = dict()
    for t in RTTList:  # GUI needs json... which uses dictionaries
        if t > 0:
            throughputDict[i] = (BUFFERSIZE * .0001) / t  #gives mb/s
            i = i + 1

    info = dict()
    info["Average Throughput"] = averageThroughput
    info["Total Time"] = totalTime

    outfile.write(json.dumps(throughputDict))
    outfile.write(json.dumps(info) + "\n")
    outfile.close()
    f = open("cgi-bin\\throughputController.txt", "w")
    f.write("stop")
    f.close()


def main():


    """
    while(1):
        f = open("throughputController.txt", "r")
        status = f.read().strip()
        f.close()
        if status == "start":
            throughput()
        else:
            continue
    """
throughput()

if __name__ == "__main__":
    main()
	


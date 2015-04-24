from socket import *
import json, time, sys


PORT = 3003  # host and client will use the same port
BUFFERSIZE = 1024
COUNT = 500  # number of packets that will be sent
HOST = "dsh-s1.info"  # this is our remote server that you will bounce packets off of

def throughputTest(fileName, fileSize, iterations, s, throughputDict, runningAverage, previousFileSize, previousN, startTime):
    n = 0

    while n < iterations:
        f = open(fileName,'rb')
        l = f.read(1024)
        t1 = time.time()
        while l:
            s.send(l)
            l = f.read(1024)
        t2 = time.time()
        if t2-t1>0:
            tempThroughput = (((fileSize)/(t2-t1)))*8/1024
            throughputDict["rows"].append({"c":[{"v":n},{"v":tempThroughput}]})
            #print tempThroughput
            midTime = time.time()
            runningAverage = (((previousFileSize*previousN + fileSize*n)/(midTime-startTime)))*8/1024
            print runningAverage
        f.close()
        n += 1
    return runningAverage

def throughput():
    print "capturing throughput\n"

    RTTList = list()
    s = socket(AF_INET, SOCK_STREAM)

    try:
        s.connect((HOST, PORT))
    except Exception, e:
        print "could not connect"

    outfile = open("throughputOutput.json", "w")
    averageOut = open("throughputOutputAverage.json", "w")


    throughputDict = dict()
    throughputDict["cols"] = [{"id":"task","type":"string"},{"id":"throughput","label":"throughput (Mbps)","type":"number"}]
    throughputDict["legend"] = {"position":"none"}
    throughputDict["rows"] = list()

    runningAverage = 0
    startTime = time.time()

    #1KB Test
    runningAverage = throughputTest("1KB.bin", 1, 1000, s, throughputDict, 0,  0, 0, startTime)

    #10KB Test
    runningAverage = throughputTest("10KB.bin", 10, 1000, s, throughputDict, 0,  1, 1000, startTime)

    #100KB Test
    runningAverage = throughputTest("100KB.bin", 100, 100, s, throughputDict, 0,  10, 1000, startTime)

    #1MB Test
    runningAverage = throughputTest("1MB.bin", 1024, 10, s, throughputDict, 0,  100, 100, startTime)

    #10MB Test
    runningAverage = throughputTest("10MB.bin", 10240, 10, s, throughputDict, 0,  1024, 10, startTime)

    #100MB Test
    runningAverage = throughputTest("100MB.bin", 102400, 1, s, throughputDict, 0,  10240, 10, startTime)

    print "Running Average: ",
    print runningAverage
    outfile.write(json.dumps(throughputDict))
    outfile.close()


def main():
    throughput()

if __name__ == "__main__":
    main()


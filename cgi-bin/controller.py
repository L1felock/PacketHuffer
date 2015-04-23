import cgi, cgitb

get = cgi.FieldStorage()
status = get.getvalue('status')

if status == "stop":
    fp = open("cgi-bin\\controller.txt", "w+")
    fp.write("stop")
    fp.close()
elif status == "start":
    fp = open("cgi-bin\\controller.txt", "w+")
    fp.write("start")
    fp.close()
elif status == "clear":
    fp = open("log.json", "w")
    #fp.write("[{\"TotalLength\": \"\", \"Protocol\": \"\", \"SequenceNumber\": \"\", \"DestinationIP\": \"\", \"WindowSize\": \"\", \"ID\": 0, \"IPVersion\": \"\", \"DestinationPort\": \"2957\", \"\": \"\", \"SourcePort\": \"\", \"SourceIP\": \"\", \"Payload\": \"\", \"AcknowledgeNumber\": \"\"}]")
    fp.write("")
    fp.close()



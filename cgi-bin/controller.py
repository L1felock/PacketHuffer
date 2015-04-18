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




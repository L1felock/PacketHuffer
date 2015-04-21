PORT = 3004
BUFSIZE = 1024

from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', PORT))
s.listen(1)

while 1:
    conn, (host, remoteport) = s.accept()
    while 1:
        data = conn.recv(BUFSIZE)
        if not data:
            break
        del data
    conn.send('OK\n')
    conn.close()


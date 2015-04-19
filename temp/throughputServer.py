PORT = 48321
BUFFERSIZE

def main():
	s = socket(AF_INET, SOCK_STREAM)
	s.bind(('', PORT))
	s.listen(1)

	while 1:
		conn, (host, remoteport) = s.accept()
		while 1:
			data = conn.recv(BUFFERSIZE)
			if not data:
				break
			del data
		conn.send('OK\n')
		conn.close()


if __name__ == "__main__":
		main()
	


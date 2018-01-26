import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 8888))

s.send(b"GET / HTTP/1.1\r\n\r\n")

relocator = s.recv(2048)

pair = str(relocator).split(':')
print(pair)

s.close()

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 8888))

s.send(b"GET / HTTP/1.1\r\n\r\n")

relocator = str(s.recv(1024))
s.close()

# The relocator currently has a prepended "b'" and an appended "'" to it,
# so we need to chop those off.
relocator = relocator[2:len(relocator)-1]

pair = str(relocator).split(':')

time.sleep(1)

sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sp.connect((pair[0], int(pair[1])))

sp.send(b"Hey there!!!\r\n\r\n")

print(sp.recv(1024))

sp.close()

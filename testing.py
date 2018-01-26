import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 8888))

s.send(b"GET / HTTP/1.1\r\n\r\n")

def handle_request(response):
        if response.error:
            print("Error:", response.error)
        else:
            print(response.body)

print (s.recv(2048))

s.close()

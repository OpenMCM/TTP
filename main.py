"""

    Theodor Johansson, Jan 2018
    Trusted Third Party (TTP) to facilitate a Multicolored Coin Market


    Behaviors:
        1. Minting coins
            - Color
            - Quantity
            - Destination
        2. Receiving bids
            - Transaction, created by client, sent to TTP
        3. Viewing bids
            - Take filtering criteria from client
            - Send all bids that fit criteria to client
        4. Receiving bid acceptances
            - Transaction, created by client, sent to TTP
            - Contains pointer to initial bid
        5. Register/Deregister external address
            - Takes a pairing (External Address,  MCMAddress, Bool)
            - Registers if Bool == true, deregisters if Bool == false
        6. Cashing out
            - TTP receives pointer to an MCM burn
            - Looks up relative address
        7. Cashing in
            - TTP receives pointer to an external burn
            - Looks up relative address
            - Mints respective coin, sends to address
"""

import sqlite3 as lite

# Example code for sqlite shamelessly plagiarized from here:
# https://pythonspot.com/python-database-programming-sqlite-tutorial/

import socket

con = None

try:
    con = lite.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print("SQLite version: %s" % data)
except lite.Error:
    print("Error %s:" % e.args[0])
    sys.exit(1)
finally:
    if con:
        con.close()

"""import tornado.web
import tornado.ioloop

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("Hey there!")
        self.write("Hello, world")
        print(self)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()"""

import socket
from multiprocessing  import Process
import mcmrequest

HOST, PORT = '', 8888

def f(name):
    print('hello', name)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)



    #p = Process(target=f, args=('bob',))
    #p.start()
    #p.join()
    #http_response = b"Hello world!"
    #client_connection.sendall(http_response)
    #client_connection.close()

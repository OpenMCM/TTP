"""

    Theodor Johansson, Jan 2018
    Trusted Third Party (TTP) to facilitate a Multicolored Coin Market

    Behaviors:
        1. Placing transactions
        2. Receiving bids
            - Transaction, created by client, sent to TTP
        3. Viewing bids (like [1], but we have to remove a bid from DB)
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
from ezsocket import create_socket
import socket
from mcmrequest import MCMRequestHandler

# Example code for sqlite shamelessly plagiarized from here:
# https://pythonspot.com/python-database-programming-sqlite-tutorial/
# I really just have it here so that I don't forget how to instantiate a
# database before I actually start implementing one.

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

HOST, PORT = '', 8888

# Basic server code stolen from https://ruslanspivak.com/lsbaws-part1/

"""listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)"""
listen_socket = create_socket((HOST, PORT))

request_distributor = MCMRequestHandler()

print('Serving MCMP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)  # This is not a request!!!
    # Change variable name to indicate the initiation of a connection

    # distribute_request() is where we gen. the new <x:y> for the client.
    request_distributor.distribute_request(request, client_connection)

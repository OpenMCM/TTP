from multiprocessing  import Process
import signal
from ezsocket import create_socket

"""

    Requests can take the following forms:
    1. Placing transactions
        "T <txbytes>"
    2. Receiving bids
        - "B <txbytes>"
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


def handle_request(request, locator):
    print(request, "\n\n", locator)

    # Listen to the locator for a connection
    # Timeout after <k> milliseconds
    listen_socket = create_socket(locator)

    def alarm_handler(signum, frame):
        listen_socket.close()
        print("Socket closed!")
        exit(1)

    # Code found at https://docs.python.org/2/library/signal.html
    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(5)

    client_connection, client_adddress = listen_socket.accept()

    request = client_coonnection.recv(1024)
    client_connection.send(b"Floop dee doo1!!\r\n\r\n")
    client_connection.close()

class MCMRequestHandler:
    def distribute_request(self, request, client_connection):

        # Generate ip:port combo
        ip = "127.0.0.1"
        port = 6666 # Hey, how about we fix this later?

        # Tell client to reconnect here
        client_connection.send((ip + ":" + str(port)).encode())

        # Close client_connection
        client_connection.close()

        # Fork process, call handle_request()
        p = Process(target=handle_request, args=(request,(ip, port),))
        p.start()
        #p.join()

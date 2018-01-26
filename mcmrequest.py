from multiprocessing  import Process
import signal
from ezsocket import create_socket

"""
    Requests can take the following forms:
    1. Placing transactions
        - "T <txbytes>"
        - return "<ack>"
    2. Receiving bids
        - "B <txbytes>"
        - return "<ack>"
    3. Viewing bids
        - "V <filtering criteria>"
        - return "<numBids>;<Bid1hex>:<Bid2hex>:..."
    4. Receiving bid acceptances
        - "A <bidIdentifier>:<txbytes>"
        - return "<ack>"
    5. Register/Deregister external address
        - "E <external address>:<MCM address>:<Bool>:<Blockchain Identifier>"
        - return "<ack>"
    6. Cashing out
        - "O <txhash>"
        - return "<ack> <txhash>"
    7. Cashing in
        - TTP receives pointer to an external burn
        - Looks up relative address
        - Mints respective coin, sends to address
        - "I <txhash>:<Blockchain Identifier>"
        - return "<ack> <txhash>"
"""


def handle_request(request, locator):

    # Listen to the locator for a connection
    # Timeout after <k> milliseconds
    print("Opening socket at", str(locator))
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

    request = client_connection.recv(1024)
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

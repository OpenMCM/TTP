from multiprocessing  import Process
import signal
from ezsocket import create_socket

"""
    Requests can take the following forms:
    1. Placing transactions
        - "T <txbytes>"
        - return "<ack>"
    2. Placing bids
        - "B <txbytes>"
        - return "<ack>"
    3. Viewing bids
        - "V <filtering criterion1>:<filtering criterion2>:..."
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

# Takes an arbitrary string as a request
# Returns a tuple (request_type, [args])
# TODO: Also asserts that the request is well-formed
def decode_request(request):
    if(request[0] == 'T'):      # A standard transaction request
        print("Request is T")

        """
            A stdtx request is well-formed iff:
                - <txbytes> is a valid transaction
        """

        return ('T', request[2:])
    elif(request[0] == 'B'):    # A bid-placement request

        """
            A bid placement request is well-formed iff:
                - <txbytes> is a valid transaction
        """

        return ('B', request[2:])
    elif(request[0] == 'V'):    # A bid-view request

        """
            A bid-view request is well-formed iff:
                - all criterion are valid?
        """

        # How do we process filtering criteria?
        return ('V', str(request[2:]).split(':'))
    elif(request[0] == 'A'):    # A bid-acceptance request

        """
            A bid-accept request is well-formed iff:
                - <bidIdentifier> is a valid bid
                - <txbytes> contains the said bid
                - <txbytes> is a valid transaction
        """

        return ('A', str(request[2:]).split(':'))
    elif(request[0] == 'E'):    # A (de?)registration request

        """
            A (de?)registration request is well-formed iff:
                - <Blockchain Identifier> is a valid bxchainID
        """

        return ('E', str(request[2:]).split(':'))
    elif(request[0] == 'O'):    # A cash-out request

        """
            A cash-out request is well-formed iff:
                - <Blockchain Identifier> is a valid bxchainID
        """

        return ('O', request[2:])
    elif(request[0] == 'I'):    # A cash-in request

        """
            A cash-in request is well-formed iff:
                - <Blockchain Identifier> is a valid bxchainID
                - <txhash> is a valid transaction to my account on bcChainiID
        """

        return ('I', str(request[2:]).split(':'))
    else:                       # Error
        print("Error decoding request: ", request)
        # What do we do here?
        exit(1)

# Takes a tuple (request_type, [args])
def execute_request(parse_out):
    request_type = parse_out[0]
    request_params = parse_out[1]
    if(request_type == 'T'):
        """ Store the transaction in the transaction table
                - Convert txbytes into DB-friendly class
                - Validate transaction
                - Hash the previous transaction
                - Insert into data table
        """
    elif(request_type == 'B'):
        # Store the bid in the bid table
        """ Store the transaction in the transaction table
                - Convert txbytes into DB-friendly class
                - Validate bid
                - Insert into data table
        """
    elif(request_type == 'V'):
        # Get set of bids, send to client
    elif(request_type == 'A'):
        # Find bid, drop from DB, store transaction in txTable
    elif(request_type == 'E'):
        # Store new address in address DB
    elif(request_type == "O"):
        # More complicated
    elif(request_type == "I"):
        # More complicated
    else:
        # Error -- this should never happen

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

    request = client_connection.recv(1024)  # Here is where we actually receive
                                            # the client's request

    # Decode the request
    parse_results = decode_request(request)

    # Execute the request

    # Format the raw output

    # Return the formatted output

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

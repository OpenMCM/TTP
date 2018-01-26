import socket

MAX_QUEUE = 100

def create_socket(locator):
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(locator)

    # Magic number alert: This '100' represents the max length of the queue
    # on this port.
    listen_socket.listen(MAX_QUEUE)
    return listen_socket

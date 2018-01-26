import multiprocessing


def handle_request(request, locator):
    print(request)

class MCMRequestHandler:
    def distribute_request(request, client_connection):
        print(request)
        # Generate ip:port combo

        # Tell client to reconnect here

        # Close client_connection

        # Fork process, call handle_request()

from http.server import HTTPServer

from forwarder_server_handler import ForwarderServerHandler


if __name__ == '__main__':
    server = HTTPServer(('', 8080), ForwarderServerHandler)
    server.serve_forever()

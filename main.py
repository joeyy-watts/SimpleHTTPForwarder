from http.server import HTTPServer

from forwarder_server_handler import ForwarderServerHandler

PORT = 8080

if __name__ == '__main__':
    print(f"Starting SimpleHTTPForwarder on port :: {PORT}")
    server = HTTPServer(('', PORT), ForwarderServerHandler)
    server.serve_forever()

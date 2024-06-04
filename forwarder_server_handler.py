from http.server import BaseHTTPRequestHandler

import requests

from utils import refresh_arp_cache, get_ip_from_alias

TARGET_ALIAS_HEADER = "X-Forward-To"


class ForwarderServerHandler(BaseHTTPRequestHandler):
    def __forward_http(self, alias, method="GET", data=""):
        # TODO: support other HTTP methods
        try:
            target_ip = get_ip_from_alias(alias)

            # initialize status
            forwarded_result = None

            try:
                forwarded_result = self.__do_forward(method, target_ip, self.path, data)
            except Exception as e:
                print(f"Failed due to :: {e}, refreshing ARP cache and retrying..")
                refresh_arp_cache()
                forwarded_result = self.__do_forward(method, target_ip, self.path, data)

            if forwarded_result.status_code < 200 or forwarded_result.status_code > 299:
                print(f"Target returned non-OK status code :: {forwarded_result.status_code}")
            else:
                print(f"Target returned OK, returning result to caller..")

            self.send_response(forwarded_result.status_code)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(forwarded_result.text, "utf-8"))
            return forwarded_result
        except Exception as e:
            print(f"Failed to forward {method} to device {alias} with path {self.path}, due to exception :: {e}")
            raise Exception(e)

    def __do_forward(self, method, target_ip, path, data=""):
        if method == "GET":
            result = requests.get("http://" + target_ip + self.path)
        elif method == "POST":
            result = requests.post("http://" + target_ip + self.path, data=data)
        else:
            self.send_response(501)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("Method not implemented", "utf-8"))
            return None

        return result

    def do_GET(self):
        print(f"GET request at path :: {self.path}")
        target_alias = self.headers[TARGET_ALIAS_HEADER]
        print(f"Forwarding to device alias :: {target_alias}")
        self.__forward_http(target_alias, method="GET")

    def do_POST(self):
        print(f"POST request at path :: {self.path}")
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        target_alias = self.headers[TARGET_ALIAS_HEADER]
        print(f"Forwarding to device alias :: {target_alias}")
        self.__forward_http(target_alias, method="POST", data=data_string)

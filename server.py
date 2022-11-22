import socket
from pprint import pprint
from io import StringIO
import sys

from app import App


class Server:
    def __init__(self, host='', port=8000, app=None):
        self.host = host
        self.port = port
        self.application = app
    
    def run(self):
        if self.application is None:
            raise Exception("Application is not set!")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)

            while True:
                conn, addr = s.accept()
                with conn:
                    req = conn.recv(1024)
                    self.handle_request(req)

                    self.response_body = self.application()(self.environ, self.start_response)

                    # print(self.status, self.resp_headers)

                    self.build_response()
                    conn.sendall(self.response)
    
    def build_response(self):
        status_line = f'{self.environ.get("SERVER_PROTOCOL")} {self.status}'
        headers = '\r\n'.join([
            f"{_[0]}: {_[1]}" for _ in self.resp_headers
        ])

        response_body_decoded = '\r\n'.join(line.decode() for line in self.response_body)

        self.response = f'{status_line}\r\n{headers}\r\n\r\n{response_body_decoded}'.encode()
        
    
    def start_response(self, status, headers):
        self.status = status
        self.resp_headers = headers

        return self.write

    def write(self):
        pass

    def handle_request(self, req):
        req = req.decode('utf-8')
        start_line, *headers, _, body = req.split('\r\n')
        method, request, version = start_line.split(' ')
        
        headers = parse_headers(headers)

        self.environ = {
            # Required WSGI keys
            'wsgi.version': (1,0),
            'wsgi.input': StringIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'REQUEST_METHOD': method,
            'PATH_INFO':    request,
            'SERVER_PROTOCOL': version,
            
            # headers
            **headers
        }




def parse_headers(headers):
    header_dict = dict()
    for header_line in headers:
        header, value = header_line.split(":", maxsplit=1)
        header_dict[f"HTTP_{header.upper().replace('-','_').replace(' ','')}"] = value.strip()
    return header_dict


wsgi = Server(host='',port=9999, app=App)
wsgi.run()
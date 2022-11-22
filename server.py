import socket
from pprint import pprint
from io import StringIO
import sys
import argparse
from app import app


class Server:
    """Implements a WSGI server"""
    def __init__(self, host='', port=8000, app=None):
        self.host = host
        self.port = port
        self.application = app      # the application associated with the wsgi server
    
    def run(self):
        if self.application is None:
            raise Exception("Application is not set!")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            """Set up the TCP socket server listening on (host, port)"""
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(1)

            print(f"Listening for requests on port {self.port}")
            while True:                 
                conn, addr = s.accept()
                with conn:
                    req = conn.recv(1024)
                    self.handle_request(req)

                    response_body = self.application(self.environ, self.start_response)

                    self.build_response(response_body)
                    conn.sendall(self.response)
    
    def build_response(self, response_body):
        """
            Builds the response based on the return from application in the standard HTTP/1.1 format
        """
        status_line = f'{self.environ.get("SERVER_PROTOCOL")} {self.status}'
        headers = '\r\n'.join([
            f"{_[0]}: {_[1]}" for _ in self.resp_headers
        ])

        response_body_decoded = '\r\n'.join(line.decode() for line in response_body)

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


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog='Server',
        description='A WSGI server',
    )
    parser.add_argument('-p','--port',default=8000)

    args = parser.parse_args()
    port = int(args.port)

    wsgi_server = Server(host='', port=port, app=app)
    wsgi_server.run()
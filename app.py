import platform
from pprint import pprint
import json

def get_sysinfo(*args, **kwargs):
    sysinfo = platform.uname()
    return {
        'name': sysinfo.node,
        'type': sysinfo.system,
        'kernel': sysinfo.version,
        'arch': sysinfo.machine
    }

def post_hello(*args, **kwargs):
    raw_data = args[0].get("wsgi.input").read().decode()
    data = json.loads(raw_data)
    pprint(data)
    return 'Hello, World'

def post_state(*args, **kwargs):
    raw_data = args[0].get("wsgi.input").read().decode()
    data = json.loads(raw_data)
    pprint(data)
    return ''

class App:
    def __init__(self):
        # self.environ = environ
        # self.start_response = start_response
        self.routes = {}
    
    def __call__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        
        if self.environ['PATH_INFO'] == '/':
            self.start_response('200 OK', [('Content-Type', 'text/plain')])
            return ['Hello World'.encode()]
        
        else:
            response_status, response_content_type, response_body = self.handle_request()
            self.start_response(response_status, [('Content-Type', response_content_type)])
            return [response_body]

    def add_url_rule(self, method, url_path, fn, *args, **kwargs):
        self.routes[(method, url_path)] = fn

    def handle_request(self):
        method, path = self.environ.get("REQUEST_METHOD"), self.environ.get("PATH_INFO")

        if not self.routes.get((method, path), None):
            return '404 NOT FOUND', 'text/plain', 'Requested resource not found'.encode()

        resp = self.routes.get((method, path))(self.environ)
        
        if isinstance(resp, dict):
            return '200 OK', 'application/json', json.dumps(resp).encode()
        else:
            return '200 OK', 'text/plain', resp.encode()


app = App()
app.add_url_rule('POST','/hello', post_hello)
app.add_url_rule('POST','/setstate', post_state)
app.add_url_rule('GET', '/sysinfo', get_sysinfo)


import platform
from pprint import pprint
import json
import views 

class App:
    def __init__(self):
        # self.environ = environ
        # self.start_response = start_response
        self.routes = {}
        self.state = None
    
    def __call__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        
        if self.environ['PATH_INFO'] == '/':
            self.start_response('200 OK', [('Content-Type', 'text/plain')])
            return ['Index'.encode()]
        
        else:
            response_status, response_content_type, response_body = self.handle_route()
            self.start_response(response_status, [('Content-Type', response_content_type)])
            return [response_body]

    def add_url_rule(self, method, url_path, fn, *args, **kwargs):
        """Build a URL-view function map"""
        self.routes[(method, url_path)] = fn

    def handle_route(self):
        try:
            self.method = self.environ.get("REQUEST_METHOD")
            self.path = self.environ.get("PATH_INFO")
            
            view_to_invoke = self.routes.get((self.method, self.path))
            request_content_type = self.environ.get("HTTP_CONTENT_TYPE") or "text/plain"

            if not view_to_invoke:
                return '404 NOT FOUND', 'text/plain', 'Requested resource not found'.encode()

            if self.method == "POST":
                request_body = self.environ.get("wsgi.input").read()
                if request_content_type == "application/json":
                    request_body = json.loads(request_body)
                resp, self.state = view_to_invoke(request_body, self.state)
            else:
                resp = view_to_invoke(self.state)
            
            # In this minimal wsgi app, we're assuming we need to return only JSON or plaintext responses
            if isinstance(resp, dict):
                return '200 OK', 'application/json', json.dumps(resp).encode()
            else:
                return '200 OK', 'text/plain', str(resp).encode()

        except Exception as e:
            return '500 Internal Server Error', 'text/plain', 'Error on server while processing your request'.encode()


app = App()
app.add_url_rule('POST','/api/hello', views.post_hello)
app.add_url_rule('POST','/api/setstate', views.post_state)
app.add_url_rule('GET','/api/currentstate', views.get_state)
app.add_url_rule('GET', '/api/sysinfo', views.get_sysinfo)

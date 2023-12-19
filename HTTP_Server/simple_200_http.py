from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_GET(self):
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send the html message
        self.wfile.write(b"Hello, this is a GET")

    def handle_request(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        print("Received request:")
        try:
            print(json.loads(post_data.decode('utf-8')))
        except json.JSONDecodeError:
            print(post_data.decode('utf-8'))

        # Send response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Received")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

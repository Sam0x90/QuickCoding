mport http.server
import socketserver
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebServer")

# Handler class for serving landing page and handling the redirection 
class WebHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
                #S erve the landing page for HTTP requests
                self.send_response(http.HTTPStatus.OK)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # Open and read HTML file
                with open('landing_sink.html', 'r') as file:
                        html_content = file.read()
                # Send the HTML content as the response
                self.wfile.write(html_content.encode('utf-8'))

# Create a socket server with both HTTP and HTTPS support
http_server = socketserver.TCPServer(('', 80), WebHandler)
http_server.allow_reuse_address = True
logger.info("HTTP server started on port 80")

#Start both servers simultaneously
try:
        http_server.serve_forever()

except KeyboardInterrupt:
        pass
finally:
        http_server.shutdown()

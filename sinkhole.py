import http.server
import socketserver
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebServer")

# Handler class for serving landing page and handling the redirection 
class WebHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.server.server_address[1] == 80:
			#S erve the landing page for HTTP requests
			self.send_response(http.HTTPStatus.OK)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			# Open and read HTML file
			with open('landing_sink.html', 'r') as file:
				html_content = file.read()

			# Send the HTML content as the response
			self.wfile.write(html_content.encode('utf-8'))
		else:
			#Redirect HTTPS to HTTP
			logger.info("Redirecting %s to HTTP" % self.path)
			self.send_response(http.HTTPStatus.MOVED_PERMANENTLY)
			self.send_header('Location', 'http://%s%s' % (self.headers['Host'], self.path))


# Create a socket server with both HTTP and HTTPS support
with socketserver.TCPServer(('', 80), WebHandler) as http_server:
	http_server.allow_reuse_address = True
	logger.info("HTTP server started on port 80")

	# Create an HTTPS server with the same handler
	with socketserver.TCPServer(('', 443), WebHandler) as https_server:
		https_server.allow_reuse_address = True
		logger.info("HTTPS server started on port 443")

		#Start both servers simultaneously
		try:
			http_server.serve_forever()
		except KeyboardInterrupt:
			pass
		finally:
			http_server.shutdown()

		try:
			https_server.serve_forever()
		except KeyboardInterrupt:
			pass
		finally:
			https_server.shutdown()

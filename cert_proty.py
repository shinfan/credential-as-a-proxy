#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import requests

PORT = 10000
GOOGLE_SERVICE_URL_HEADER = 'goog_service_url'
HOST_HEADER = 'host'

class GoogleServiceProxy(SimpleHTTPServer.SimpleHTTPRequestHandler):

	# The handler for all 'GET' request.
    def do_GET(self):
    	request_headers = self.headers.dict
    	google_service_url = request_headers.pop(GOOGLE_SERVICE_URL_HEADER, None)
    	# host header is set to http://localhost:PORT by the request
    	# and will confuse the outbound http request if not removed.
    	request_headers.pop(HOST_HEADER, None)
        
    	google_service_response = requests.get(google_service_url, headers=request_headers)

        # Set status.
    	self.send_response(google_service_response.status_code)
    	# Set headers.
    	for key in google_service_response.headers:
    		# SimpleHTTPRequestHandler provides the 'Content-Length' header.
    		# An 'Illegal chunked encoding' errors will come up 
    		# if 'Transfer-Encoding: chuncked' is further added.
    		if 'Transfer-Encoding' not in key:
    			self.send_header(key, google_service_response.headers[key])
    	self.end_headers()
    	# Set body of the response to the proxy caller.
        self.wfile.write(google_service_response.text)

httpd = SocketServer.ForkingTCPServer(('', PORT), GoogleServiceProxy)
print ("Now serving at " + str(PORT))
httpd.serve_forever()
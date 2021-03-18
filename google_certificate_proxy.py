#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import requests

PORT = 10000
GOOGLE_SERVICE_URL_HEADER = 'goog_service_url'
HOST_HEADER = 'host'
CONTENT_LENGTH_HEADER = 'content-length'

class GoogleCertificateProxy(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        """The handler for all GET requests."""
    	request_headers, google_service_url, _ = self._process_request_headers() 
        
    	google_service_response = requests.get(google_service_url, headers=request_headers)

        self._send_response(google_service_response)

    def do_POST(self):
        """The handler for all POST requests."""
        request_headers, google_service_url, content_length = self._process_request_headers()
        request_data = self._extract_request_data(content_length)

        google_service_response = requests.post(google_service_url, headers=request_headers, data=request_data)

        self._send_response(google_service_response)

    def _process_request_headers(self):
        """Processes the request headers.
           
        1. Extracts Google service URL from the header.
        2. Extracts the content length if presents.
        3. Removes the host header.

        Returns:
            [request_headers, google_service_url, content_length]
        """
        request_headers = self.headers.dict
        google_service_url = request_headers.pop(GOOGLE_SERVICE_URL_HEADER, None)

        if CONTENT_LENGTH_HEADER in request_headers:
          content_length = int(request_headers.get(CONTENT_LENGTH_HEADER))
        else:
          # CONTENT_LENGTH_HEADER will not present if the request does not contain data.
          content_length = None

        # host header is set to http://localhost:PORT by the request
        # and will confuse the outbound http request if not removed.
        request_headers.pop(HOST_HEADER, None)

        return request_headers, google_service_url, content_length

    def _extract_request_data(self, content_length):
        """Extracts the request data based on content_length.
        
        Returns:
            Request data if content_length is presented. Otherwise, returns None.
        """
        if content_length is not None:
          return self.rfile.read(content_length)
        else:
          return None      

    def _send_response(self, response):
        """Sends the response back to the caller of the proxy.
 
        The response sent includes the status code, response headers and the respone data.
        """

        # Set status.
        self.send_response(response.status_code)
        # Set headers.
        for key in response.headers:
            # SimpleHTTPRequestHandler provides the 'Content-Length' header.
            # An 'Illegal chunked encoding' errors will come up 
            # if 'Transfer-Encoding: chuncked' is further added.
            if 'Transfer-Encoding' not in key:
                self.send_header(key, response.headers[key])
        self.end_headers()
        # Set body of the response to the proxy caller.
        self.wfile.write(response.text)            


httpd = SocketServer.ForkingTCPServer(('', PORT), GoogleCertificateProxy)
print ("Now serving at " + str(PORT))
httpd.serve_forever()
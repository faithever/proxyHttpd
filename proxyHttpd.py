import http.server
import socketserver
import sys
import requests
import os
from urllib.parse import urlparse

fileServerAddr = sys.argv[1]
fileServerPort = sys.argv[2]

class ProxyHttpd (http.server.BaseHTTPRequestHandler):
	""" __init__ 이 있으면, do_GET function이 불리지 않는다.
	def __init__(self, request, client_address, server):
		print("ProxyHttpd __init__")
		print("Request: {}".format(request))
		super(ProxyHttpd, self)
	"""

	def do_GET(self):
		parsed_path = urlparse(self.path)
		filepath = parsed_path.path
		print("The requested file : {}".format(filepath))
		if len(filepath) > 0 and not filepath in "/favicon.ico":
			url = "http://"+fileServerAddr+":"+fileServerPort+filepath
			response = requests.get(url, stream=True)
			print("Connecting to {} to download the file {}".format(url, filepath))
			if response.status_code == 200:
				contentLength = len(response.content)
				print("Successfully download file {}. Content size {}".format(filepath,contentLength))
				self.send_response(200)
				self.send_header('Content-type', "binaries")
				self.send_header('Content-Length', str(contentLength))
				self.end_headers()
				written_data_size = 0
				for data in response.iter_content(chunk_size=1024):
					if data:
						written_data_size += len(data)
						self.wfile.write(data)
				print("Sent Byte is {}".format(written_data_size))
		else:
			print("The file not Found")
			self.send_response(404)
			self.end_headers()
			message = "File not Found"
			self.wfile.write(message.encode())
			#self.wfile.write(bytes("File Not Found", "UTF-8"))
			
	def do_PUT(self):
		parsed_path = urlparse(self.path)
		filepath = parsed_path.path
		fileName = os.path.basename(filepath)
		url = "http://"+fileServerAddr+":"+fileServerPort+filepath
		contentLength = int(self.headers["Content-Length"])
		headers = {
			"Content-Length":str(contentLength),
			"Content-Type":"application/binary",
		}
		print("The Url: {}".format(url))
		print("The content length:{}".format(contentLength))
		data = self.rfile.read(contentLength)
		response = requests.put(url, data=data, headers=headers)
		print(response)
		self.send_response(200)
		self.end_headers()
		

	
server_address = ('', 9999)		
httpd = http.server.HTTPServer(server_address, ProxyHttpd)
print("Listen port {}".format(9999))
#http.server.HTTPServer는 socketserver.TCPServer와 같다.
#httpd = socketserver.TCPServer(server_address, ProxyHttpd)
try :
	httpd.serve_forever()
except KeyboardInterrupt:
	sys.exit("Program stop because of KeyboardInterrupt !!")
	

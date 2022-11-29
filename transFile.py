import sys
import os
import getopt
import http.server
from urllib.parse import urlparse


class HttpHandler(http.server.BaseHTTPRequestHandler):
   @classmethod
   def setConfig(cls, dirs, keyword):
      cls.dirs = dirs
      cls.keyword = keyword
      print("Enter setConfig with dirs:{} and keyword:{}".format(cls.dirs, cls.keyword))

   def findFile(self, targetFile):
      #print("Enter with dirs({}) targetFile({})".format(self.dirs,targetFile))
      for dirname in self.dirs:
         for (dirpath, dirs, files) in os.walk(dirname):
            for f in files:
               if f == targetFile:
                  return os.path.join(dirpath,f)

   def do_GET(self):
      parsedPath = urlparse(self.path)
      targetFile = os.path.basename(parsedPath.path)
      resultFile = ''
      if len(targetFile) > 0 and not targetFile in "/favicon.ico":
         print("Start to findFile with targetFile({})".format(targetFile))
         resultFile = self.findFile(targetFile)

      if resultFile:
         fileSize = os.path.getsize(resultFile)
         oFile = open(resultFile, 'rb')
         data = oFile.read()
         print(f'fileSize : {fileSize}')
         self.send_response(200)
         self.send_header('Content-type','binaries')
         self.send_header('Content-Length', str(fileSize))
         self.end_headers()
         self.wfile.write(data)

   def do_PUT(self):
      parsedPath = urlparse(self.path)
      filePath = parsedPath.path
      dirName = os.path.dirname(filePath)
      fileName = os.path.basename(filePath)
      fullPath = os.path.join('/tmp/pool'+dirName, fileName)
      contentLength = int(self.headers['Content-Length'])
      if os.path.exists(fullPath):
         print("File {} exists and remove".format(fullPath))
         os.remove(fullPath)

      print(f'fullPath: {fullPath}, filePath:{filePath}, fileName:{fileName} and size is {contentLength} ')
      with open(fullPath, 'wb') as outFile:
         outFile.write(self.rfile.read(contentLength))
         os.chmod(fullPath, 0o755)
      self.send_response(200)
      self.end_headers()


class TransFile():
   def __init__ (self, port, dirs, keyword):
      self.port = port
      self.dirs = dirs
      self.keyword = keyword

   def run(self):
      server_address = ('', int(self.port))
      self.httpd = http.server.HTTPServer(server_address, HttpHandler)
      HttpHandler.setConfig(self.dirs,self.keyword)
      try:
         self.httpd.serve_forever()
      except KeyboardInterrupt:
         print("KeybardInterrup happen")
         sys.exit("EXIT")


def main(argv):
   keyword = '' 
   try:
      opts, args = getopt.getopt(argv,"p:k:", ["dirs="])
   except getopt.error as message:
      print("getopt Error: {}".format(message))
      sys.exit(2)

   print("opts=" + str(opts))
   print("args=" + str(args))

   for opt, val in opts:
      #print("opt:{} and val:{}".format(opt, val))
      if opt == '-p':
         port = val
      if opt == '-k':
         keyword = val
      if opt == '--dirs': 
         dirs = val.split(',') #make list

   tf = TransFile(port, dirs, keyword)
   tf.run()


if __name__ == '__main__':
   main(sys.argv[1:])



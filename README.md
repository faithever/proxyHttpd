# proxyHttpd and transFile
Lets say you want to download a file in a server which you cannot connect directly.
However fortunately you can connect to PC or whatever which can connect to the server you want to connect.

You run the proxyHttpd on the PC between you and the server and you run the transFile on the server.
ProxyHttpd requests the transFile to download files you want to get.

For example :
The transFile daemon run on the 172.16.0.200:9000
The proxyHttpd daemon runs on the 192.168.100.2:9999
The file you want to download is hello.html which should be at the 172.16.0.200

your browser can request like this "http://192.168.100.2:99999/hello.html.


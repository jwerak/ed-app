from http.server import BaseHTTPRequestHandler, HTTPServer
from types import FrameType
import sys
import os
import signal
import datetime

from version import __version__

HOST_NAME = '0.0.0.0'
PORT = int(os.getenv('PORT', 8080))
ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEV')
VERSION = __version__

startTime = datetime.datetime.now()
requestsCounterGet = 0
requestsCounterPost = 0

class AppServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global requestsCounterGet

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            requestsCounterGet += 1
            msg = getMessage(ENVIRONMENT, VERSION)
            self.wfile.write(bytes(msg, 'utf8'))

        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type','text/plain; version=0.0.4')
            self.end_headers()

            msg = getMetrics()
            self.wfile.write(bytes(msg, 'utf8'))

    def do_POST(self):
        global requestsCounterPost
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            requestsCounterPost += 1
            msg = getMessage(ENVIRONMENT, VERSION)
            self.wfile.write(bytes(msg, 'utf8'))
            

def shutdown_handler(signal: int, frame: FrameType) -> None:
    print('Exiting process.', flush=True)
    sys.exit(0)

def getMessage(env, version):
    uptime = getUptime() 
    return f'''<html>
<head><title>Example Edge Application</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
<style>
div {{text-align: center;}}
</style>
</head>
<body>
<div>
<h1>Hello, World!</h1>
<p>ENVIRONMENT: <b>{env}</b></p>
<p>VERSION: <b>{version}</b></p>
<p>UPTIME: <b>{uptime} seconds</b></p>
</div>
</body>
</html>
'''

def getUptime():
    """
    Returns the number of seconds since the program started.
    """
    uptime = datetime.datetime.now() - startTime
    return uptime.seconds

def getMetrics():
    return f'''
    http_requests_total{{method="get"}} {requestsCounterGet}
    http_requests_total{{method="post"}} {requestsCounterPost}
    '''



if __name__ == '__main__':
    server = HTTPServer((HOST_NAME, PORT), AppServer)
    print(f'Server started http://{HOST_NAME}:{PORT}')
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    server.serve_forever()

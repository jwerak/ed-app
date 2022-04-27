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

class AppServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        msg = getMessage(ENVIRONMENT, VERSION)
        self.wfile.write(bytes(msg, 'utf8'))

def shutdown_handler(signal: int, frame: FrameType) -> None:
    print('Exiting process.', flush=True)
    sys.exit(0)

def getMessage(env, version):
    uptime = getUptime() 
    return f'''<html>
<head><title>Example Edge Application</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>
<body>
<h1>Hello, World!</h1>
<p>ENVIRONMENT: <b>{env}</b></p>
<p>VERSION: <b>{version}</b></p>
<p>UPTIME: <b>{uptime} seconds</b></p>
</body>
</html>
'''

def getUptime():
    """
    Returns the number of seconds since the program started.
    """
    uptime = datetime.datetime.now() - startTime
    return uptime.seconds

startTime = datetime.datetime.now()

if __name__ == '__main__':
    server = HTTPServer((HOST_NAME, PORT), AppServer)
    print(f'Server started http://{HOST_NAME}:{PORT}')
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    server.serve_forever()

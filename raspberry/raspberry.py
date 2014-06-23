from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from shutil import copyfile
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time, subprocess, signal

PORT = 8000

class Gopro:
    STATUS_OFF="OFF"
    STATUS_ON="ON"

    def __init__(self):
        self.status = self.STATUS_OFF

    def getStatus(self):
        return self.status

    def start(self):
        print "start gopro"

        if (self.status != self.STATUS_OFF):
            return

        # start
        self.status = self.STATUS_ON

        return

    def stop(self):
        print "stop gopro"

        if (self.status != self.STATUS_ON):
            return

        # stop
        self.status = self.STATUS_OFF

        return

    def cleanup(self):
        print "clean gopro"

        return


class GoproServer(HTTPServer):

    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.gopro = Gopro()

    def signal_term_handler(self, signal, frame):
        print 'got SIGTERM'

        self.gopro.cleanup()

        sys.exit(0)


class GoproHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        return

    def do_GET(self):
        gopro = self.server.gopro

        # read status file
        status = gopro.getStatus()

        if (self.path == '/gopro/start' and status == gopro.STATUS_OFF):
            gopro.start()

        if (self.path == '/gopro/stop' and status == gopro.STATUS_ON):
            gopro.stop()

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        # return status
        self.wfile.write(gopro.getStatus())

        return


try:
    httpd = GoproServer(("", PORT), GoproHandler)
    print "serving at port", PORT
    httpd.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	httpd.gopro.cleanup()
	httpd.socket.close()

signal.signal(signal.SIGTERM, httpd.signal_term_handler)

 

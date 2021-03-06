from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from shutil import copyfile
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time, subprocess, signal
import RPi.GPIO as GPIO

PORT = 8000

class Gopro:
    STATUS_OFF="OFF"
    STATUS_ON="ON"

    # Set GPIO pins
    # outputs
    MODE_BTN = 23    # Goes to GoPro pin 12

    # inputs
    STATUS_PIN = 25  # Goes to GoPro pin 24


    def __init__(self):
        self.status = self.STATUS_OFF
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.MODE_BTN,  GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.STATUS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def getStatus(self):
        return self.status

    def start(self):
        print "start gopro"

        if (self.status != self.STATUS_OFF):
            return

        # start
        self.status = self.STATUS_ON
        self.turnon();

        return

    def stop(self):
        print "stop gopro"

        if (self.status != self.STATUS_ON):
            return

        # stop
        self.status = self.STATUS_OFF
        self.turnoff()

        return

    def stopSilent(self):
        print "stop silent gopro"

        # stop
        self.status = self.STATUS_OFF

        return

    def cleanup(self):
        print "clean gopro"
        GPIO.cleanup()

        return

    def turnon(self):
        print(GPIO.input(self.MODE_BTN))
        GPIO.output(self.MODE_BTN, False)
        print(GPIO.input(self.MODE_BTN))
        time.sleep(1)
        GPIO.output(self.MODE_BTN, True)
        print(GPIO.input(self.MODE_BTN))
        time.sleep(2)

    def turnoff(self):
        print(GPIO.input(self.MODE_BTN))
        GPIO.output(self.MODE_BTN, False)
        print(GPIO.input(self.MODE_BTN))
        time.sleep(3)
        GPIO.output(self.MODE_BTN, True)
        print(GPIO.input(self.MODE_BTN))
        time.sleep(2)

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

        if (self.path == '/gopro/stop_silent' and status == gopro.STATUS_ON):
            gopro.stopSilent()

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

 

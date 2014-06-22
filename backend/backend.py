from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT = 8000

class PhotoBooth:
    STATUS_READY="READY"
    STATUS_COUNT_DOWN="COUNT DOWN"
    STATUS_RECORDING="RECORDING"
    STATUS_PROCESSING="PROCESSING"

    def getStatus(self):
        # read status file
        # if status in STATUSES
            # return status
        # else
            # return ready
        return self.STATUS_READY

    def takePicture(self):
        # if status is not status ready
            # return

        # count down
        return

    def countDown(self):
        # set status to countdown
        # set camera mode to camera
        # wait count down time
        # start recording
        return

    def recording(self):
        # set status to recording
        # start camera
        # wait recording time
        # stop camera
        # start processing
        return

    def processing(self):
        # set status to processing
        # set camera mode to usb
        # copy last video to directory
        # remove last video from gopro directory
        # cut picture one from video
        # cut picture two from video
        # cut picture three from video
        # cut picture four from video
        # set status to ready
        return

class PhotoBoothServer(HTTPServer):

    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.photoBooth = PhotoBooth()


class PhotoBoothHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        photoBooth = self.server.photoBooth
        # read status file
        status = photoBooth.getStatus()
        # if status file is ready
        if (status == photoBooth.STATUS_READY):
            # take a picture
            photoBooth.takePicture

        # return status
        self.sendStatus(photoBooth.getStatus())
        return


    def sendStatus(self,status):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(status)
        return


try:
    httpd = PhotoBoothServer(("", PORT), PhotoBoothHandler)

    print "serving at port", PORT
    httpd.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	httpd.socket.close()

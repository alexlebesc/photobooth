from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from shutil import copyfile
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time, subprocess

PORT = 8000

class PhotoBooth:
    STATUS_READY="READY"
    STATUS_COUNT_DOWN="COUNT DOWN"
    STATUS_RECORDING="RECORDING"
    STATUS_PROCESSING="PROCESSING"

    def __init__(self):
        self.status = self.STATUS_READY

    def getStatus(self):
        return self.status

    def takePicture(self):
        print "takePicture"

        # if status is not status ready
        if (self.status != self.STATUS_READY):
            return

        # count down
        self.countDown();

        return

    def countDown(self):
        countDownTime = 5;

        print "count down"

        # set status to countdown
        self.status=self.STATUS_COUNT_DOWN;

        # set camera mode to camera
        self.goproModeCamera()

        # start camera
        self.startCamera()

        # wait count down time
        time.sleep(countDownTime)

        # start recording
        self.recording();

        return

    def recording(self):
        recordingTime = 5;

        print "recording"

        # set video ID
        self.videoId = time.time()

        # set status to recording
        self.status = self.STATUS_RECORDING;

        # wait recording time
        time.sleep(recordingTime)

        # stop camera
        self.stopCamera()

        # start processing
        self.processing();

        return

    def processing(self):
        processingTime = 15

        print "processing"

        # set status to processing
        self.status = self.STATUS_PROCESSING;

        # set camera mode to usb
        self.goproModeUSB()

        # copy last video to directory
        video = self.copyVideo();

        # remove last video from gopro directory
        if (video):
            self.removeGoproVideo();

            cutTiming = [1,2,3,4]
            for timing in cutTiming:
                self.cutPicture(video, timing)

        # set status to ready
        self.status = self.STATUS_READY;

        return

    def startCamera(self):
        print "start camera"

        command = 'curl  http://192.168.33.20:8000/gopro/start'

        subprocess.call(command, shell=True)

        return

    def stopCamera(self):
        print "stop camera"

        command1 = 'curl  http://192.168.33.20:8000/gopro/stop'

        subprocess.call(command1, shell=True)

        return

    def goproModeCamera(self):
        print "gopro mode camera"
        currentDir =  os.path.dirname(os.path.realpath(__file__))

        command1 = 'curl  http://192.168.33.20:8000/gopro/stop_silent'
        command2 = 'sudo ' + currentDir + '/modeStorage_stop.sh'
        command3 = 'sudo ' + currentDir + '/modeCamera.sh'

        subprocess.call(command1, shell=True)
        subprocess.call(command2, shell=True)
        subprocess.call(command3, shell=True)
        time.sleep(5)

        return

    def goproModeUSB(self):
        print "gopro mode USB"
        currentDir =  os.path.dirname(os.path.realpath(__file__))

        command1 = 'sudo ' + currentDir + '/modeStorage_start.sh'
        subprocess.call(command1, shell=True)

        self.startCamera()
        time.sleep(3)

        return

    def copyVideo(self):
        print "copy video from gopro to computer"

        # set computer video directory
        videoDir = os.path.dirname(os.path.realpath(__file__)) + '/video'

        video = self.findLastVideo()

        if (video):
            # copy last video in computer directory
            copyfile(video, videoDir + '/' + os.path.basename(video) )
            return videoDir + '/' + os.path.basename(video)

        return

    def findLastVideo(self):
        lastVideo = ''

        # set gopro directory
        goproDir = os.path.dirname(os.path.realpath(__file__)) + '/gopro'

        # find last video in gopro directory
        entries = (os.path.join(goproDir, fn) for fn in os.listdir(goproDir))
        entries = ((os.stat(path), path) for path in entries)

        entries = ((stat[ST_CTIME], path) for stat, path in entries if S_ISREG(stat[ST_MODE]))

        for cdate, path in sorted(entries, reverse=True):
            if (path.endswith('.MP4')):
                lastVideo = path
                break

        return lastVideo

    def removeGoproVideo(self):
        print "Remove gopro video"

        # set gopro directory
        # find last video in gopro directory
        # remove last video from gopro directory
        video = self.findLastVideo()
        videoLRV = video.replace('.MP4', '.LRV')
        videoTHM = video.replace('.MP4', '.THM')

        print 'remove',video
        os.remove(video)
        os.remove(videoLRV)
        os.remove(videoTHM)

        return

    def cutPicture(self, video, timing):
        print "cut picture at",timing, "sec"
        image = os.path.dirname(os.path.realpath(__file__)) + '/images/' + str(self.videoId) + '_' + str(timing) + '.jpeg'
        command = 'ffmpeg -i ' + video +  ' -ss ' + str(timing) + ' -t 00:00:1 -r 1 -qscale:v 1 ' + image

        subprocess.call(command, shell=True)

        return

    def cleanup(self):
        print "clean backend"

        return

class PhotoBoothServer(HTTPServer):

    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.photoBooth = PhotoBooth()


class PhotoBoothHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        return

    def do_GET(self):
        photoBooth = self.server.photoBooth

        # read status file
        status = photoBooth.getStatus()

        # if status file is ready
        if (self.path == '/' and status == photoBooth.STATUS_READY):
            # take a picture
            photoBooth.takePicture()

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        # return status
        self.sendStatus(photoBooth.getStatus())

        return


    def sendStatus(self,status):
        self.wfile.write(status)
        return


try:
    httpd = PhotoBoothServer(("", PORT), PhotoBoothHandler)
    print "serving at port", PORT
    httpd.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	httpd.socket.close()

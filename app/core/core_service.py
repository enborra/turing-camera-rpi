import signal
import time


class CoreService(object):
    _kill_now = False


    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def start(self):
        while True:


            try:
                print("[PEEK] Taking a photo..")

                from picamera import PiCamera

                camera = PiCamera()
                camera.rotation = 90
                camera.capture('/home/pi/projects/img.jpg')
            except Exception:
                print("[PEEK] Skipping taking a photo. Not a supported OS.")

            time.sleep(10)

            if self._kill_now:
                break

    def stop(self):
        pass

    def exit_gracefully(self,signum, frame):
        self._kill_now = True

    # def setup(self):
    #     GPIO.setwarnings(False)
    #
    #     GPIO.setmode(GPIO.BOARD)
    #     GPIO.setup(7, GPIO.OUT)
    #     GPIO.setup(11, GPIO.OUT)
    #     GPIO.setup(12, GPIO.OUT)
    #     GPIO.setup(13, GPIO.OUT)

    # def pour_liquid(self):
    #     self._pump_state = self.PUMP_RUNNING
    #
    #     GPIO.output(12, GPIO.HIGH)
    #     GPIO.output(11, GPIO.LOW)
    #     GPIO.output(7, GPIO.HIGH)
    #     GPIO.output(13, GPIO.HIGH)

    # def stop_pouring(self):
    #     GPIO.output(12, GPIO.LOW)
    #     GPIO.output(11, GPIO.LOW)
    #     GPIO.output(7, GPIO.LOW)
    #     GPIO.output(13, GPIO.LOW)
    #
    #     self._pump_state = self.PUMP_STOPPED

import signal
import time

try:
    from picamera import PiCamera
except Exception:
    pass

class CoreService(object):
    _kill_now = False
    _camera = None


    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        try:
            self._camera = PiCamera()
        except Exception:
            self._camera = None

    def start(self):
        while True:


            if self._camera:
                print("[CAMERA-RPI] Taking a photo..")

                self._camera.rotation = 180
                self._camera.capture('/home/pi/projects/img.jpg')

            else:
                print("[CAMERA-RPI] Skipping taking a photo. Not a supported OS.")

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

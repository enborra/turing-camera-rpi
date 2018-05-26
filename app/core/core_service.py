import threading
import json
import paho.mqtt.client as mqtt

import signal
import time

import io
from PIL import Image
import base64
import cStringIO


try:
    from picamera import PiCamera
except Exception:
    pass


class CoreService(object):
    _kill_now = False

    _comm_client = None
    _comm_delay = 0
    _thread_comms = None
    _thread_lock = None

    _camera = None

    _system_channel = '/system'
    _data_channel = '/camera/rpi'


    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        try:
            self._camera = PiCamera()
        except Exception:
            self._camera = None

    def start(self):
        self._comm_client = mqtt.Client(
            client_id="service_camera_rpi",
            clean_session=True
        )

        self._comm_client.on_message = self._on_message
        self._comm_client.on_connect = self._on_connect
        self._comm_client.on_publish = self._on_publish
        self._comm_client.on_subscribe = self._on_subscribe

        self._thread_lock = threading.RLock()

        self._thread_comms = threading.Thread(target=self._start_thread_comms)
        self._thread_comms.setDaemon(True)
        self._thread_comms.start()

        while True:
            if self._camera:
                print("[CAMERA-RPI] Starting filestream.")

                # Capture raw camera image and create a PIL image object

                stream = io.BytesIO()

                print("[CAMERA-RPI] Taking a photo..")

                self._camera.start_preview()
                time.sleep(2)
                self._camera.capture(stream, format='jpeg')

                stream.seek(0)
                image = Image.open(stream)

                buffer = cStringIO.StringIO()
                image.save(buffer, format='JPEG')
                img_str = base64.b64encode(buffer.getvalue())

                # print('****\n' + img_str + '\n****')

                self.output(img_str, self._data_channel)

            else:
                print("[CAMERA-RPI] Skipping taking a photo. Not a supported OS.")

            time.sleep(10)

            if self._kill_now:
                break

    def _on_connect(self, client, userdata, flags, rc):
        self.output('{"sender": "service_camera_rpi", "message": "Connected to GrandCentral."}')

    def _on_message(self, client, userdata, msg):
        msg_struct = None

        try:
            msg_struct = json.loads(msg.payload)

        except:
            pass

    def _on_publish(self, mosq, obj, mid):
        pass

    def _on_subscribe(self, mosq, obj, mid, granted_qos):
        self.output('{"sender": "service_camera_rpi", "message": "Successfully subscribed to GrandCentral /system channel."}')

    def _on_log(self, mosq, obj, level, string):
        pass

    def _connect_to_comms(self):
        print('Connecting to comms system..')

        try:
            self._comm_client.connect(
                'localhost',
                1883,
                60
            )

        except Exception, e:
            print('Could not connect to local GranCentral. Retry in one second.')

            time.sleep(1)
            self._connect_to_comms()

    def _start_thread_comms(self):
        print('Comms thread started.')

        self._thread_lock.acquire()

        try:
            self._connect_to_comms()

        finally:
            self._thread_lock.release()

        print('Connected to comms server.')

        while True:
            self._thread_lock.acquire()

            try:
                if self._comm_delay > 2000:
                    self._comm_client.loop()
                    self._comm_delay = 0

                else:
                    self._comm_delay += 1

            finally:
                self._thread_lock.release()

    def output(self, msg, channel=_system_channel):
        if self._comm_client:
            self._comm_client.publish(channel, msg)

    def stop(self):
        pass

    def exit_gracefully(self,signum, frame):
        self._kill_now = True

import sys

from core import CoreService

c = CoreService()

try:
    print("[CAMERA-RPI] Booting.")

    c.start()

except KeyboardInterrupt:
    print("[CAMERA-RPI] Shutting down.")

    c.stop()

    try:
        sys.stdout.close()
    except:
        pass

    try:
        sys.stderr.close()
    except:
        pass

except Exception as e:
    print( "Error: %s" % str(e) )

    c.stop()

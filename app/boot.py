import sys

from core import CoreService

c = CoreService()

try:
    print("[PEEK] Booting.")

    c.start()

except KeyboardInterrupt:
    print("[PEEK] Shutting down.")

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

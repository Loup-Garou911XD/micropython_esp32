import os
from machine import reset
import esp

esp.osdebug("LOG_WARN")

print("\n"*20+"bootstrapping")

try:
    from bootstrap import *
    print("bootstrapping successfull")
except Exception as err:
    print(err)

import webrepl
webrepl.start()

try:
    import test.py #for testing stuff at boot
except ImportError:
    pass
except Exception as err:
    print(err)

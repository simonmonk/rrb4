# Attach: SR-04 Range finder

from rrb4 import *


rr = RRB4()

try:
    while True:
        distance = rr.get_distance()
        print(distance)
        time.sleep(0.2)
finally:
    print("Exiting")
    rr.cleanup()
    

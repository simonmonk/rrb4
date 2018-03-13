from rrb4 import *
from random import randint

rrb = RRB4(6,6)
stop = False
x = 1

try:
    while True:
        rrb.set_R(randint(-1, 1))
        rrb.set_L(randint(-1, 1))
        print(x)
        x += 1
        time.sleep(1)
        
finally:
    GPIO.cleanup()
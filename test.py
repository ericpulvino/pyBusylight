#!/usr/bin/env python
import time
from pybusylight import busylight
from pybusylight import sounds

#import pprint
#pprint.pprint(busylight().available_colors())

test=busylight()

#test.send()
#
#time.sleep(1)
#
#test.turn_off()
#test.blink(rgb=(255,0,0),interval=0.05,count=5)
#test.blink(color='orange',interval=0.05,count=5)
#test.blink(color='yellow',interval=0.05,count=5)
#test.blink(color='green',interval=0.05,count=5)
#test.blink(rgb=(0,0,255),interval=0.05,count=5)
#test.blink(color='purple',interval=0.05,count=5)
#
#test.set_rgb((0,255,0))
#
#print(test.get_rgb())
#
#test.send()
#
#time.sleep(1)
#
test.set_color('salmon')
#test.blink(count=10)

test.pulse(count=5,color='blue')

test.pulse(count=5,color='goldenrod')

#for sound in sounds:
#    print('sending %s'%sound)
#    test.set_sound(sound=sounds[sound],volume=1)
#    test.send()
#    time.sleep(5)
#    test.turn_off()



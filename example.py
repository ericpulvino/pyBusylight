#!/usr/bin/env python
import time
from pybusylight import busylight
from pybusylight import sounds

try:
    print('Connect to the Busylight...')
    bl=busylight()
except ValueError:
    print('\nBusylight not found, is it connected?...')
    exit(1)

print('\nSend basic white for 5 seconds.')
bl.send()
time.sleep(5)

print('\nTurn Off All elements of the busylight (both light and sound) for 2 seconds.')
bl.turn_off()
time.sleep(2)

print('\nSet the light to a color (GREEN) via RGB (0,255,0).')
bl.set_rgb((0,255,0))
bl.send()
time.sleep(5)

print('\nSet the light to a named color (SALMON).')
bl.set_color('salmon')
bl.send()
time.sleep(5)

rgb_value=bl.get_rgb()
print('\nGet the RGB value for the color that is currently set --> %s%s%s'%(rgb_value[0],rgb_value[1],rgb_value[2]))

print('\nBlink the light 10 times with whatever color value is currently set using the default interval of 0.5 seconds.')
bl.blink(count=10)

print('\nBlink the light with and RGB color (255,0,0) 5 times waiting half a second between blinks.')
bl.blink(rgb=(255,0,0),interval=0.5,count=5)

print('\nBlink the light with a named color (orange) 10 times waiting 1/20th of a second between blinks')
bl.blink(color='orange',interval=0.05,count=5)

print('\nPulse the light 5 times with the current color. Each pulse cycle is about ~0.78 seconds.')
bl.pulse(count=5)

print('\nPulse the light 5 times with a named color (goldenrod).')
bl.pulse(count=5,color='goldenrod')

print('\nPulse the light 5 times with an RGB color (0,0,255).')
bl.pulse(count=5,rgb=(0,0,255))

print('\nPlaying each of the supported sounds for 5 seconds...')
for sound in sounds:
    print('\n        playing the "%s" at volume level 2 of 7'%sound)
    bl.set_sound(sound=sounds[sound],volume=2)
    bl.send()
    time.sleep(5)
    bl.turn_off()

print('\nSetting a color and letting the color time-out automatically (after 30 seconds).')
bl.set_color('mauve')
bl.send()

exit(0)

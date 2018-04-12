#!/usr/bin/env python
import time
from pybusylight import busylight
from pybusylight import sounds

try:
    print('Connect to the Busylight...')
    bl=busylight()
except ValueError:
    print('Busylight not found, is it connected?...')
    exit(1)

print('Send basic white for 5 seconds.')
bl.send()
time.sleep(5)

print('Turn Off All elements of the busylight (both light and sound) for 2 seconds.')
bl.turn_off()
time.sleep(2)

print('Set the light to a color (GREEN) via RGB (0,255,0).')
bl.set_rgb((0,255,0))
bl.send()
time.sleep(5)

print('Set the light to a named color (SALMON).')
bl.set_color('salmon')
bl.send()
time.sleep(5)

print('Get the rgb value for the color that is currently set --> %s'%bl.get_rgb())

print('Blink the light 10 times with whatever color value is currently set using the default interval of 0.5 seconds.')
bl.blink(count=10)

print('Blink the light with and RGB color (255,0,0) 5 times waiting half a second between blinks.')
bl.blink(rgb=(255,0,0),interval=0.5,count=5)

print('Blink the light with a named color (orange) 10 times waiting 1/20th of a second between blinks')
bl.blink(color='orange',interval=0.05,count=5)

print('Pulse the light 5 times with the current color. Each pulse cycle is about ~0.78 seconds.')
bl.pulse(count=5)

print('Pulse the light 5 times with a named color (goldenrod).')
bl.pulse(count=5,color='goldenrod')

print('Pulse the light 5 times with an RGB color (0,0,255).')
bl.pulse(count=5,rgb=(0,0,255))

print('Playing each of the supported sounds for 5 seconds...')
for sound in sounds:
    print('        playing the "%s" at volume level 2 of 7'%sound)
    bl.set_sound(sound=sounds[sound],volume=2)
    bl.send()
    time.sleep(5)
    bl.turn_off()

print('Setting a color and letting the color time-out automatically (after 30 seconds).')
bl.set_color('mauve')
bl.send()

exit(0)

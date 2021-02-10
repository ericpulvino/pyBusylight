from pybusylight.color_constants import colors
import binascii
import usb.core
import usb.util
import signal
import time
import sys
import struct

def signal_handler(signal, frame):
    print('\nCaught CTRL+C turning off.')
    busylight().turn_off()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class busylight:

    def __init__(self, debug=False, usb_vendor=None, usb_product=None):
        self.ep = None 
        self.debug = debug
        self.__connect_busylight__(usb_vendor, usb_product)
        self.red = 255
        self.green = 255
        self.blue = 255
        self.sound = 0
        self.volume = 0
        self.max_valid_sound = 15

    def __connect_busylight__(self, usb_vendor, usb_product):
        try:
            if usb_vendor is None or usb_product is None: # probe mode
                # Device IDs taken from https://github.com/ericpulvino/pyBusylight/issues/2
                for i in [0x3bca, 0x3bcd, 0x3bcb, 0x3bcc, 0x3bc0, 0xf848]:
                    dev = usb.core.find(idVendor=0x27bb, idProduct=i)
                    if dev:
                        break
            else:
                dev = usb.core.find(idVendor=usb_vendor, idProduct=usb_product)
                
        except NoBackendError:
            print("""ERROR: PyUSB needs at least one of the supported backends installed.
    If you're on a MAC you can install libusb via:
        $ brew install libusb

    On Windows you can follow the info here.
        https://github.com/walac/pyusb/blob/master/README.rst#installing

    On Ubuntu 16.04/18.04
    sudo apt-get install libusb-1.0-0 """)
            exit(1)

        if dev is None: raise ValueError('Device not found')
        dev.reset()
        if dev.is_kernel_driver_active(0) == True:
                dev.detach_kernel_driver(0)

        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()
        intf = cfg[(0,0)]

        self.ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        assert self.ep is not None

    def __build_buff__(self):

        # The protocol can be found here:
        # https://github.com/porsager/busylight/blob/master/Busylight.API.rev.2.2.-.22052015.pdf
        
        # Start with an empty array
        byte_buf = bytearray(64)

        # command
        byte_buf[0] = 0b00010000 # 0b00010aaa: Jump to step aaa when the step is executed.
        
        # repeat
        byte_buf[1] = 1 # Execute this step for repeat number of times [1..255] 
        
        # color
        byte_buf[2] = degamma[self.red]
        byte_buf[3] = degamma[self.green]
        byte_buf[4] = degamma[self.blue]

        # on_time
        byte_buf[5] = 255 # ON time in 0.1 second steps [0..255] <=> 0-25.5sec

        # off time
        byte_buf[6] = 255 # OFF time in 0.1 second steps [0..255] <=> 0-25.5sec

        # ringtone
        # bitwise interpretation: 0bcbbbbeee
        # c: on/off
        # bbbb: sound
        # eee: volume (0=stop, 111=highest)
        byte_buf[7] = 0 

        
        byte_buf[7] |= 128 # always change audio
        
        if self.sound:        
            byte_buf[7] |= ((self.sound & self.max_valid_sound) << 3)
            byte_buf[7] |= self.volume & 7


        # It is possible to repeat command definitions, but we leave the other
        # fields blank here.

        # sensitivity
        byte_buf[56] = 16 # 0=high sensitivity 31=low sensitivity

        # timeout in seconds (1-30)
        byte_buf[57] = 5

        # triggertime in milliseconds (1-250)
        byte_buf[58] = 1

        # unused
        byte_buf[59] = 0xff
        byte_buf[60] = 0xff
        byte_buf[61] = 0xff
        
        
        # calculate check sum
        _sum = sum(byte_buf)            
        byte_buf[62] = _sum >> 8
        byte_buf[63] = _sum & 255

        if self.debug:
            print(byte_buf)
        
        return byte_buf

    def pulse(self,pulse_length=None,rgb=None,color=None,count=None):
        if color:
            self.set_color(color)
        elif rgb:
            self.set_rgb(rgb)

        if count:
            try:
                count = int(count)
            except:
                print('Provided blink count is not an integer.')
                exit(1)

            
        color_val=self.get_rgb()
        red_activation=float(color_val[0])/float(255)
        red_step=red_activation/32.0
        green_activation=float(color_val[1])/float(255)
        green_step=green_activation/32.0
        blue_activation=float(color_val[2])/float(255)
        blue_step=blue_activation/32.0

        current_count=0
        while True:
            if count:
                current_count += 1
                if current_count > count: return
            red_value,green_value,blue_value=(0,0,0)
            for i in range(0,32):
                red_value = red_value+red_step
                green_value = green_value+green_step
                blue_value = blue_value+blue_step
                #print('red: %s green: %s blue: %s'%(int(round(red_value*255.0)),int(round(green_value*255.0)),int(round(blue_value*255.0))))
                self.red,self.green,self.blue=(int(round(red_value*255.0)),int(round(green_value*255.0)),int(round(blue_value*255.0)))
                self.send()
                time.sleep(0.01)
            #print('top')
            for i in range(31,-1,-1):
                red_value = red_value-red_step
                green_value = green_value-green_step
                blue_value = blue_value-blue_step
                #print('red: %s green: %s blue: %s'%(int(round(red_value*255.0)),int(round(green_value*255.0)),int(round(blue_value*255.0))))
                self.red,self.green,self.blue=(int(round(red_value*255.0)),int(round(green_value*255.0)),int(round(blue_value*255.0)))
                self.send()
                time.sleep(0.01)
            #print('bottom')

    def available_colors(self):
        all_colors=[]
        for color in colors: all_colors.append((color,colors[color]))
        return all_colors

    def set_sound(self, sound=1, volume=0):
        try:
            if int(sound) <= self.max_valid_sound: self.sound=sound
            else:
                print('Sound is not a valid value (0<=sound<=%d).'%(self.max_valid_sound))
                exit(1)
            if int(volume) in range(0,8): self.volume=volume
            else:
                print('Volume must be an integer from 0-7.')
                exit(1)
        except:
            print('Sound or volume is not an integer.')
            exit(1)

    def set_rgb(self,rgb):
        for i in range(0,3):
            if rgb[i] >255 or rgb[i] < 0:
                print('Bad RGB value.')
                exit(1)
        try:
            self.red,self.green,self.blue=rgb
        except:
            print('Failed to collect RGB value.')
            exit(1)

    def set_color(self,color):
        try:
            self.set_rgb(colors[color])
        except:
            print('Invalid Color, see busylight.available_colors()')
            exit(1)

    def get_rgb(self):
        return (self.red,self.green,self.blue)
        

    def blink(self,rgb=None,color=None,interval=0.5,count=None):
        try:
            interval = float(interval)
        except:
            print('Invalid interval value. Must be something which can be typed as a float.')
            return

        if count:
            try:
                count = int(count)
            except:
                print('Provided blink count is not an integer.')
                exit(1)

        if color:
            self.set_color(color)
        elif rgb:
            self.set_rgb(rgb)

        color_val=self.get_rgb()

        current_count=0        
        while True:
            if count:
                current_count += 1
                if current_count > count: return
            self.red,self.green,self.blue=color_val
            self.send()
            time.sleep(interval)
            self.red,self.green,self.blue=(0,0,0)
            self.send()
            time.sleep(interval)


    def turn_off(self):
        self.red=0
        self.green=0
        self.blue=0
        self.sound=0
        self.volume=0
        self.send()

    def send(self):
        self.ep.write(self.__build_buff__())

degamma = [
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
  2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
  6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 11, 11,
  11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,
  19, 19, 20, 21, 21, 22, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28,
  29, 29, 30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 37, 38, 39, 40,
  40, 41, 42, 43, 44, 45, 46, 46, 47, 48, 49, 50, 51, 52, 53, 54,
  55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
  71, 72, 73, 74, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89,
  90, 91, 93, 94, 95, 96, 98, 99,100,102,103,104,106,107,109,110,
  111,113,114,116,117,119,120,121,123,124,126,128,129,131,132,134,
  135,137,138,140,142,143,145,146,148,150,151,153,155,157,158,160,
  162,163,165,167,169,170,172,174,176,178,179,181,183,185,187,189,
  191,193,194,196,198,200,202,204,206,208,210,212,214,216,218,220,
  222,224,227,229,231,233,235,237,239,241,244,246,248,250,252,255
]

sounds={"off": 0,
        "openoffice": 1,
        "quiet": 2,
        "funky": 3,
        "fairytale": 4,
        "kuandotrain": 5,
        "telephonenordic": 6,
        "telephoneoriginal": 7,
        "telephonepickmeup": 8,
        "unknown": 9,
        "buzz": 11
        }

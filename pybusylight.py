#!/usr/bin/python

import usb.core
import usb.util
import signal
import time
import sys

def signal_handler(signal, frame):
    print('\nCaught CTRL+C turning off.')
    halt_busylight=busylight()
    halt_busylight.turn_off()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

class busylight:

    def __init__(self):
        self.ep = None 
        self.__connect_busylight__()
        self.red = 255
        self.green = 255
        self.blue = 255
        self.sound = 128
        self.volume = 0

    def __connect_busylight__(self):
        dev = usb.core.find(idVendor=0x04d8, idProduct=0xf848)

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
        buff = ("\x10\x00%s%s%s\x00\x00%s\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x04\xab"%(
                   chr(self.red),
                   chr(self.green),
                   chr(self.blue),
                   chr(int(self.sound)+int(self.volume))
                   )
               )
        return buff

    def pulse(self):
        while True:
            for i in range(0,256,8):
                self.green = degamma[i] 
                self.send()
                time.sleep(0.01)
            for i in range(255,-1,-8):
                self.green = degamma[i]
                self.send()
                time.sleep(0.01)

    def turn_off(self):
        self.red=0
        self.green=0
        self.blue=0
        self.sound=128
        self.volume=0
        self.send()

    def send(self):
        buff = self.__build_buff__()
        self.ep.write(buff)

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

sounds={"off":128,
        "OpenOffice":136,
        "Quiet":144,
        "Funky":152,
        "FairyTale":160,
        "KuandoTrain":168,
        "TelephoneNordic":176,
        "TelephoneOriginal":184,
        "TelephonePickMeUp":192,
        "Buzz":216
        }

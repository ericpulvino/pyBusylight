#!/usr/bin/python

import usb.core
import usb.util
import time

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

    def send_signal(self):
        buff = self.__build_buff__()
        self.ep.write(buff)

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

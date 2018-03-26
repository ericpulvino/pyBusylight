# pyBusylight

pyBusylight is a native python library which controls Kuando Busylight devices. It is intented to serve as a foundational component which can be integrated into other higher-level scripts.

pyBusylight makes use of PyUSB to control Busylight and used extensive cues from the [busylight node library](https://github.com/porsager/busylight).

## Dependencies
* signal
* pyusb

## Most Simple Use Case
```
user@hostname$ sudo python

import pybusylight

test=pybusylight.busylight()

test.send()
```

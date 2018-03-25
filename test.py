#!/usr/bin/env python

import time
import pybusylight

test=pybusylight.busylight()

test.send()

time.sleep(1)

test.turn_off()

test.pulse()

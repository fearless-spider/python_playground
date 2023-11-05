#!/usr/bin/env python3
"""
GetDeviceAngle - 0xD7
GetCurFanPumpSpeed - 0xD8
GetFanPumpCurve - 0xD9
GetFanAndPumpMode - 0xDD
SendCpuInfo - 0xE0
SendCpuName - 0xE1
SendDisplay - 0xE2
SetFanPumpMode - 0xE5
WritingFlash - 0xE7
SetDeviceAngle - 0xE8

byte magic (Always 0x99)
byte command/response
and then the command/response data, padded out to 0x100 or 0x1800.

For the status response (0xDA on the first device), it looks like a bunch of null separated values for the fan speed, pump speed, an unknown 4 byte, and the liquid temperature.

for setting the fan and pump mode
99(magic) e5(set fan pump op) 01(01=fan,02=pump) 06(mode)
mode code as follow:
07 zero
00 balance
05 performance
06 quiet
04 max
02 default
01 custom

below not tested yet:
for setting the custom curve for fan, it seems to be the following:
99 e6 01 01 00(degree) 03 ef(speed 1007) ...... (seems up to 4 (degree,speed) tuples)

for setting the custom curve for pump, it might be the following:
99 e6 04 02 00(degree) 03 ef(speed 1007) ...... (seems up to 4 (degree,speed) tuples)

for reading cooler stat
99 da .....
return
99 da 62 03(fan speed) 00 f5 04(pump speed) 00 20 25 1f a1 00 1a(liquid degree)

99 d9 01 .... (read custom fan curve)
99 d9 02 .... (read custom pump curve)

Bytes [8] and [9] appear to be the fan and pump duty percentages, respectively. Thus, you are running the fan and pump at 32/37% in that example.

Additionally, if you're going to start setting pump curve, you should be checking the model + firmware and clamping the rpm where necessary? Gigabyte seems to set the lower boundary at 750rpm, and the upper at 2800 or 3200 depending on firmware version. (There are also some model checks involved, but they are against what looks like OEM versions of the cooler with different usb PID.)
"""
import time

import psutil
import usb.core
import usb.util


def get_cpu_temp():
    t = psutil.sensors_temperatures()
    for x in ["coretemp"]:
        if x in t:
            return int(t[x][0].current)
    print("Warning: Unable to get CPU temperature!")
    return 0


def makecpuupdatestr():
    # change to your number of core
    ncore = 10
    # change to your number of threads
    nthread = 20
    # change to your cpu Ghz
    ghz = 5.3

    cputemp = "{:02x}".format(get_cpu_temp())
    ncorestr = "{:02x}".format(ncore)
    nthreadstr = "{:02x}".format(nthread)
    ghz1 = "{:02x}".format(int(ghz))
    ghz2 = "{:02x}".format(int((ghz - int(ghz)) * 10))
    print(ghz1)
    print(ghz2)
    data = "99e000" + cputemp + "18" + ghz1 + ghz2 + ncorestr + nthreadstr
    print(data)
    data += "0" * (6144 * 2 - len(data))
    barray = bytes.fromhex(data)
    return barray


def readhexdump(filename):
    f = open(filename, "r")
    data = f.read()
    barray = bytes.fromhex(data)
    return barray


# find our device
dev = usb.core.find(idVendor=0x1044, idProduct=0x7A4D)

# was it found?
if dev is None:
    raise ValueError("Device not found")

bdata = makecpuupdatestr()
endpoint = dev[0][(0, 0)][0]
endpoint2 = dev[0][(0, 0)][1]
interface = 0
print(dev)
if dev.is_kernel_driver_active(interface) is True:
    # tell the kernel to detach
    print(dev[0])
    dev.detach_kernel_driver(interface)
    usb.util.claim_interface(dev, interface)
    while True:
        try:
            bdata = makecpuupdatestr()
            dev.write(endpoint2, bdata)
        except usb.core.USBError as e:
            print(e)
        time.sleep(2)
else:
    print("Not active")
    dev.attach_kernel_driver(interface)

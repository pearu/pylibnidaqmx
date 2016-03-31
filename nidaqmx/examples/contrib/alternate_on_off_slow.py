# with relatively loose timing constraints
# turn on and off a digital output

from __future__ import division
from numpy import *
import labdaq.daqmx as daqmx
import labdaq.daq as daq
import threading,time

def min2sec(minutes):
    return minutes*60.0

###### setup script parameters ########

long_duration = min2sec(1.0) # twenty minutes
duration = 25.0 # sec
onvoltage = 5.0
offvoltage = 0.0
onstate = False
gCurrentTimer = None
state_verbal= {True:'On', False: 'Off'}


def change_voltage(onstate):
    print onstate
    if onstate:
        daq.set_voltage_ch0(onvoltage)
    else :
        daq.set_voltage_ch0(offvoltage)

def cycle(onstate=onstate):
    print "hi! Starting up loop of alternating on voltage %f with off voltage of %f every %f seconds or %f minutes" % (onvoltage, offvoltage, duration, sec2min(duration))
    while 1:
        onstate = not onstate
        change_voltage(onstate)
        time.sleep(duration)
        # gCurrentTimer = threading.Timer(duration, cycle, (onstate,))
        

if __name__=='__main__':
    cycle()

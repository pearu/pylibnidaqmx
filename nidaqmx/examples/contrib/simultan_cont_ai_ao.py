# -*- coding: utf-8 -*-
# do simultaneous analog input and output
import time
from ctypes import *
import numpy as np
import nidaqmx
import labdaq.daqmx as mx


def getCurWritePos(task):
    cur_wp = mx.uInt64(0)
    mx.CHK(mx.ni.DAQmxGetWriteCurrWritePos(otask, byref(cur_wp)))
    return cur_wp.value

def relativeTo(task,newval=None):
    """
    newval may be either DAQmx_Val_FirstSample 10424
    or
    DAQmx_Val_CurrWritePos (10430)
    """
    if not newval:
        val = mx.uInt64(0)
        mx.ni.DAQmxGetWriteRelativeTo(task, byref(val))
        return val.value
    else:
        mx.CHK(mx.ni.DAQmxSetWriteRelativeTo(task,newval))

def resetRelativeTo(task):
    mx.CHK(mx.ni.DAQmxResetWriteRelativeTo(task,newval))
        

##########
analog_output_term = r'Dev1/ao0'
analog_input = r'Dev1/ai15' # connect analog input to this terminal, customize as you wish
TERMINALEND = 'nrse' # consider 'rse' (referenced single-ended),'nrse'
                     # (non-referenced single ended) for configuration
                     # of analog input

samplerate = 2000
nsamples = 1000 # if samplemode = 'continuous' used to determine buffer size
samplemode = 'continuous' # or 'continuous'

outputdata = np.arange(nsamples,dtype='float64') 
outputdata = np.sin(0.2*outputdata)
output2 = np.sin(0.5*np.arange(nsamples,dtype='float64') )
print outputdata.shape




itask = nidaqmx.AnalogInputTask()
itask.create_voltage_channel(analog_input, min_val=0.0,max_val=10.0,
                             terminal=TERMINALEND)
itask.configure_timing_sample_clock(rate=samplerate,
                                    sample_mode=samplemode,
                                    samples_per_channel=nsamples)


# print "input task buffer size", itask.get_buffer_size()
# print itask.get_read_current_position()
# get_regeneration

otask = nidaqmx.AnalogOutputTask()

otask.create_voltage_channel(analog_output_term, min_val=-10.0,max_val=10.0)

otask.configure_timing_sample_clock(source=r'ai/SampleClock',
                                    rate=samplerate,
                                    sample_mode=samplemode,
                                    samples_per_channel=nsamples)

otask.write(outputdata,auto_start=False)


# start them both
cur_wp = mx.uInt64(0)
otask.start()
itask.start()
d1=itask.read(samples_per_channel=500)
time.sleep(1.0)
print "current read position", itask.get_read_current_position()
mx.ni.DAQmxGetWriteCurrWritePos(otask, byref(cur_wp))
otask.write(output2)
after = getCurWritePos(otask)
time.sleep(0.1)
# d2 = itask.read(samples_per_channel=500)
# itask.wait_until_done(10.0)
# print "otask.get_bufsize()",otask.get_bufsize()
print "before cur_wp:",cur_wp.value, "and after:", after
print "relativeTo:", relativeTo(otask)
print "done"


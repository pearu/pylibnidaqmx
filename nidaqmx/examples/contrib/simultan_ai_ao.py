# -*- coding: utf-8 -*-
# do simultaneous analog input and output
import numpy as np
import nidaqmx

analog_output_term = r'Dev1/ao0'
analog_input = r'Dev1/ai15' # connect analog input to this terminal, customize as you wish
TERMINALEND = 'nrse' # consider 'rse' (referenced single-ended),'nrse'
                     # (non-referenced single ended) for configuration
                     # of analog input

samplerate = 10000
nsamples = 1000 # if samplemode = 'continuous' used to determine buffer size
samplemode = 'finite' # or 'continuous'

#outputdata = np.linspace(0.0,1000.0, num=nsamples) # assumine default to float64
outputdata = np.arange(nsamples,dtype='float64') # assumine default to float64
outputdata = np.sin(0.2*outputdata)

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
otask.start()
itask.start()

itask.wait_until_done(10.0)
print "done"

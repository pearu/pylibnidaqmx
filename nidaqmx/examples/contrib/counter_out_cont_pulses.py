from __future__ import division
import numpy as np
import nidaqmx


nsamples = 1000
samplerate = 1000
counter = nidaqmx.CounterOutputTask()

device = nidaqmx.libnidaqmx.Device('Dev1')
print "counter output channels", device.get_counter_output_channels()
print "counter input channels", device.get_counter_input_channels()


counter.create_channel_frequency(r'Dev1/ctr0', name='counter0', freq=samplerate)
counter.configure_timing_implicit(sample_mode='continuous', samples_per_channel=nsamples)
counter.start()


import time
print "waiting 10 seconds"
time.sleep(10.0*(nsamples/samplerate))
print "I don't think it should be done"
print "is task done?", counter.is_done()
print "stopping task now"
counter.stop()

# output a sine wave of 1000 samples to terminal /Dev1/ao0
# while simultaneously outputing a 1ms digital pulse every 5 ms (duty cycle 20%)
# using correlated digital output based off the analog sample clock

# need to start the dio task first!

import numpy as np
import nidaqmx
nsamples = 1000
samplerate = 1000

adata = 9.95*np.sin(np.arange(nsamples,dtype=np.float64)*2*np.pi/nsamples)

atask = nidaqmx.AnalogOutputTask()
atask.create_voltage_channel('Dev1/ao0', min_val=-10.0,max_val=10.0)
atask.configure_timing_sample_clock(rate=samplerate,sample_mode='finite', samples_per_channel=1000)
atask.write(adata, auto_start=False)
# ok that's tee'd up

ddata = np.zeros(nsamples, dtype=np.uint8)
ddata[0:nsamples:5]=1

dotask = nidaqmx.DigitalOutputTask()
dotask.create_channel('Dev1/port0/line0', name='line0')
#print "dotask info:", dotask.get_info_str(True)
print "atask info:", atask.get_info_str()
# note must use r'ao/SampleClock' (can't prefix with /Dev1/
dotask.configure_timing_sample_clock(source=r'ao/SampleClock',rate=1000,sample_mode='finite',samples_per_channel=1000)
dotask.write(ddata, auto_start=False)
dotask.start()

atask.start()

print "press return to end"
c =raw_input()



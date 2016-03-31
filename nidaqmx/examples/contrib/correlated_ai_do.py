# using correlated digital output based off the analog sample clock
# 

# need to start the dio task first!
import time
import numpy as np
import nidaqmx

# some useful parameters
nsamples = 5000 # about 5 sec
samplerate = 1000
TERMINALEND = 'nrse' # consider 'rse' (referenced single-ended),'nrse' (non-referenced single ended)
                     # 'diff', or 'pseudodiff' as other options, can look at panel for hints
analog_input = r'Dev1/ai15' # connect analog input to this terminal, customize as you wish
ndigital = 2 # number of digital channels
digital_output_str = r'Dev1/port0/line6:7'

itask = nidaqmx.AnalogInputTask()
itask.create_voltage_channel(analog_input, min_val=0.0,max_val=10.0, terminal=TERMINALEND)
itask.configure_timing_sample_clock(rate=samplerate,sample_mode='finite',samples_per_channel=nsamples)


# ok that's tee'd up
# assume that these are uint8

ddata = np.zeros(nsamples*ndigital, dtype=np.uint8)
onarr = np.ones(ndigital,dtype=np.uint8)
offarr = np.zeros(ndigital,dtype=np.uint8)
## for interleaved layout
# ddata[0:10] = 1 # turn both on for 5 ticks
# ddata[10:2*nsamples:100]=1  # now turn both on for 3ms every 100ms
# ddata[11:2*nsamples:100]=1
# ddata[12:2*nsamples:100]=1
# ddata[13:2*nsamples:100]=1
# ddata[14:2*nsamples:100]=1
# ddata[15:2*nsamples:100]=1
# ddata[16:2*nsamples:100]=1
# # turn both off
# ddata[-1] = 0
# ddata[-2] = 0
## for by_channel layout

# 2ms pulses at 10hz
ddata[0:nsamples:100] = 1
ddata[1:nsamples:100] = 1
ddata[nsamples-1] = 0
# 2nd channel setup, offset by 40ms do same thing
offset = 40
ddata[nsamples+offset:ndigital*nsamples:100] =1
ddata[nsamples+offset+1:ndigital*nsamples:100] =1
ddata[-1] = 0


dotask = nidaqmx.DigitalOutputTask()
dotask.create_channel(digital_output_str, name='line67' )
#print "dotask info:", dotask.get_info_str(True)
print "itask info:", itask.get_info_str()
# note must use r'ao/SampleClock' (can't prefix with /Dev1/
dotask.configure_timing_sample_clock(source=r'ai/SampleClock',rate=samplerate,sample_mode='finite',samples_per_channel=nsamples)
dotask.write(ddata, auto_start=False, layout='group_by_channel')
             # layout='group_by_scan_number')
print "digital task info:"
print dotask.get_info_str()
dotask.start()

print "starting"
itask.start()
time.sleep(nsamples/samplerate)
data = itask.read() # get data

print "press return to end"
c =raw_input()



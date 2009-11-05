
from nidaqmx import AnalogInputTask
import numpy as np

task = AnalogInputTask()
task.create_voltage_channel('Dev1/ai16', terminal = 'rse', min_val=-10.0, max_val=10.0)
task.configure_timing_sample_clock(rate = 1000.0)

def callback (task, event_type, samples, callback_data):
    print 
    data = task.read(samples, samples_per_channel=samples,
                     fill_mode='group_by_scan_number')
    print 'Acquired %s samples' % (len (data))
    print data[:10]
    return 0

def callback_done(task, status, callback_data):
    print 'callback_done, status=',status
    return 0

#task.register_every_n_samples_event(callback, samples = 100)
#task.register_done_event(callback_done)

task.start()

if 1:
    from pylab import plot, show
    data = task.read(3000, fill_mode='group_by_channel')
    plot (data)
    show ()

raw_input('Acquiring samples continuously. Press Enter to interrupt..')

#task.stop() # gives 'pure virtual method called' abort message

del task

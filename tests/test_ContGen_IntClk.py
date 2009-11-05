
from nidaqmx import AnalogOutputTask
import numpy as np
data = 9.95*np.sin(np.arange(1000, dtype=np.float64)*2*np.pi/1000)
task = AnalogOutputTask()
task.create_voltage_channel('Dev1/ao2', min_val=-10.0, max_val=10.0)
task.configure_timing_sample_clock(rate = 1000.0)
task.write(data)
task.start()
raw_input('Generating voltage continuously. Press Enter to interrupt..')
task.stop()
del task

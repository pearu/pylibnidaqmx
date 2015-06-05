PyLibNIDAQmx provides a Python package `nidaqmx` that wraps the [NI-DAQmx driver software](http://www.ni.com/dataacquisition/nidaqmx.htm) for Python using [ctypes](http://docs.python.org/library/ctypes.html).

The package is tested with NI-DAQwx library version 8.0 using [PCI-6602](http://sine.ni.com/nips/cds/view/p/lang/en/nid/1123) and [PCIe-6259](http://sine.ni.com/nips/cds/view/p/lang/en/nid/201814) cards on openSUSE 11.0 Linux.

# Basic usage #

The `nidaqmx` Python package provides the following classes:

> [AnalogInputTask](http://sysbio.ioc.ee/download/software/pylibnidaqmx/generated/nidaqmx.AnalogInputTask.html), [AnalogOutputTask](http://sysbio.ioc.ee/download/software/pylibnidaqmx/generated/nidaqmx.AnalogOutputTask.html), [DigitalInputTask](http://sysbio.ioc.ee/download/software/pylibnidaqmx/generated/nidaqmx.DigitalInputTask.html), [DigitalOutputTask](http://sysbio.ioc.ee/download/software/pylibnidaqmx/generated/nidaqmx.DigitalOutputTask.html),  [CounterInputTask](http://sysbio.ioc.ee/download/software/pylibnidaqmx/generated/nidaqmx.CounterInputTask.html), [CounterOutputTask](http://sysbio.ioc.ee/download/software/pylibnidaqmx/generated/nidaqmx.CounterOutputTask.html).

These classes expose NI-DAQ tasks to Python environment. The task instances provide methods to create channels, setting timing and triggering properties and
reading and writing data.

See also [PyLibNIDAQmx Documentation](http://sysbio.ioc.ee/download/software/pylibnidaqmx/index.html).

Here follows an example how to generate voltage:

```
>>> from nidaqmx import AnalogOutputTask
>>> import numpy as np
>>> data = 9.95*np.sin(np.arange(1000, dtype=np.float64)*2*np.pi/1000)
>>> task = AnalogOutputTask()
>>> task.create_voltage_channel('Dev1/ao2', min_val=-10.0, max_val=10.0)
>>> task.configure_timing_sample_clock(rate = 1000.0)
>>> task.write(data, auto_start=False)
>>> task.start()
>>> raw_input('Generating voltage continuously. Press Enter to interrupt..')
>>> task.stop()
>>> del task
```

and example how to measure and plot the voltage:

```
>>> from nidaqmx import AnalogInputTask
>>> import numpy as np
>>> task = AnalogInputTask()
>>> task.create_voltage_channel('Dev1/ai16', terminal = 'rse', min_val=-10.0, max_val=10.0)
>>> task.configure_timing_sample_clock(rate = 1000.0)
>>> task.start()
>>> data = task.read(2000, fill_mode='group_by_channel')
>>> del task
>>> from pylab import plot, show
>>> plot (data)
>>> show ()
```

If `Dev1/ao2` and `Dev1/ai16` are directly connected then you should see
two sine waves plotted to screen.

For more examples, follow the link in [Issue 4](http://code.google.com/p/pylibnidaqmx/issues/detail?id=4) (thanks to Chris Lee-Messer).
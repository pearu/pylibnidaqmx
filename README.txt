=====================================================
PyLibNIDAQmx - a Python wrapper to libnidaqmx library
=====================================================

:Authors:

  Pearu Peterson <pearu.peterson AT gmail DOT com>

:Download:

  https://github.com/pearu/pylibnidaqmx

:Documentation:

  https://sysbio.ioc.ee/download/software/pylibnidaqmx/

:License:

  New BSD License

History
=======

 * Project published on November 5, 2009.


Installation
============

To use pylibnidaqmx, the following is required:

  * Python 2.5 or newer
  * numpy package
  * libnidaqmx library

To install pylibnidaqmx, unpack the archive file, change to the
pylibnidaqmx source directory ``PyLibNIDAQmx-?.?*`` (that contains
setup.py file and nidaqmx package), and run::

  python setup.py install

Basic usage
===========

The nidaqmx Python package provides the following classes:
AnalogInputTask, AnalogOutputTask, DigitalInputTask, DigitalOutputTask,
CounterInputTask, CounterOutputTask that can be used to create
NI-DAQ tasks and they have methods to create channels, setting
timing and triggering properties and reading and writing data.

Here follows an example how to generate voltage:

>>> from nidaqmx import AnalogOutputTask
>>> import numpy as np
>>> data = 9.95*np.sin(np.arange(1000, dtype=np.float64)*2*np.pi/1000)
>>> task = AnalogOutputTask()
>>> task.create_voltage_channel('Dev1/ao2', min_val=-10.0, max_val=10.0)
>>> task.configure_timing_sample_clock(rate=1000.0)
>>> task.write(data, auto_start=False)
>>> task.start()
>>> raw_input('Generating voltage continuously. Press Enter to interrupt..')
>>> task.stop()
>>> del task

and example how to measure and plot the voltage:

>>> from nidaqmx import AnalogInputTask
>>> import numpy as np
>>> task = AnalogInputTask()
>>> task.create_voltage_channel('Dev1/ai16', terminal = 'rse', min_val=-10.0, max_val=10.0)
>>> task.configure_timing_sample_clock(rate=1000.0)
>>> task.start()
>>> data = task.read(2000, fill_mode='group_by_channel')
>>> del task
>>> from pylab import plot, show
>>> plot (data)
>>> show ()

If Dev1/ao2 and Dev1/ai16 are directly connected then you should see
two sine waves plotted to screen.

Additional documentation is available online in PyLibNIDAQmx website.

Help and bug reports
====================

You can report bugs at the pylibnidaqmx issue tracker:

  https://github.com/pearu/pylibnidaqmx/issues

Any comments and questions can be sent also to the authors.



"""
.. currentmodule:: nidaqmx

The :mod:`nidaqmx` package provides the following classes:

.. autosummary::

  AnalogInputTask
  AnalogOutputTask
  DigitalInputTask
  DigitalOutputTask
  CounterInputTask
  CounterOutputTask

that expose NIDAQmx tasks to Python environment. The instances of
these task classes provide methods to create channels, to set timing
and triggering properties, as well as to read or write data.

Example usage
=============

The following example demonstrates how to create an analog output
task that generates voltage to given channel of the NI card::

>>> from nidaqmx import AnalogOutputTask
>>> import numpy as np
>>> data = 9.95*np.sin(np.arange(1000, dtype=np.float64)*2*np.pi/1000)
>>> task = AnalogOutputTask()
>>> task.create_voltage_channel('Dev1/ao2', min_val=-10.0, max_val=10.0)
>>> task.configure_timing_sample_clock(rate = 1000.0)
>>> task.write(data)
>>> task.start()
>>> raw_input('Generating voltage continuously. Press Enter to interrupt..')
>>> task.stop()
>>> del task

The generated voltage can be measured as well when connecting the corresponding
channels in the NI card::

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

that should plot two sine waves.
"""


from .libnidaqmx import AnalogInputTask, AnalogOutputTask, DigitalInputTask, DigitalOutputTask, CounterInputTask, CounterOutputTask

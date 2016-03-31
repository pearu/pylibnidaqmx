#!/usr/bin/env python
# -*- python-mode -*-
"""
"""
# Author: Pearu Peterson
# Created: August 2009

from __future__ import division
import os
import sys
import time

### START UPDATE SYS.PATH ###
### END UPDATE SYS.PATH ###

from ioc.optparse_gui import OptionParser
from optparse import OptionGroup

from nidaqmx import AnalogOutputTask
from nidaqmx.optparse_options import get_method_arguments, set_ao_options
import numpy as np

def runner (parser, options, args):
    task = AnalogOutputTask()
    args, kws = get_method_arguments('create_voltage_channel', options)
    phys_channel = kws['phys_channel']
    task.create_voltage_channel (**kws)

    channels = task.get_names_of_channels()
    if not channels:
        print 'No channels specified'
        return

    args, kws = get_method_arguments('configure_timing_sample_clock', options)
    clock_rate = kws.get('rate', 1000.0)

    if not task.configure_timing_sample_clock(**kws):
        return

    args, kws = get_method_arguments('ao_write', options)
    layout = kws.get('layout', 'group_by_scan_number')

    if options.ao_task=='sin':
        min_val = task.get_min(phys_channel)
        max_val = task.get_max(phys_channel)
        samples_per_channel = clock_rate / len(channels)
        x = np.arange(samples_per_channel, dtype=float)*2*np.pi/samples_per_channel
        data = []
        for index, channel in enumerate(channels):
            data.append(0.5*(max_val+min_val) + 0.5*(max_val-min_val)*np.sin(x-0.5*index*np.pi/len(channels)))
        data = np.array(data)
        if layout=='group_by_scan_number':
            data = data.T
    else:
        raise NotImplementedError (`options.ai_task`)
    print 'samples available/written per channel= %s/%s ' % (data.size//len(channels), task.write(data.ravel(), **kws))

    if not options.ao_write_auto_start:
        task.start()
    try:
        time.sleep(options.ao_task_duration)
    except KeyboardInterrupt, msg:
        print 'Caught Ctrl-C.'
    task.stop()
    del task

def main ():
    parser = OptionParser()
    set_ao_options(parser)
    if hasattr(parser, 'runner'):
        parser.runner = runner
    options, args = parser.parse_args()
    runner(parser, options, args)
    return

if __name__=="__main__":
    main()

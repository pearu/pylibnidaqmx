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

import numpy as np

from ioc.optparse_gui import OptionParser
from optparse import OptionGroup

from nidaqmx import AnalogInputTask
from nidaqmx.optparse_options import get_method_arguments, set_ai_options

def runner (parser, options, args):
    task = AnalogInputTask()

    print 'Created AnalogInputTask %s (task.value=%s)' % (task, task.value)

    args, kws = get_method_arguments('create_voltage_channel', options)
    print 'create_voltage_channel', kws
    task.create_voltage_channel (**kws)

    channels = task.get_names_of_channels()
    if not channels:
        print 'No channels specified'
        return

    args, kws = get_method_arguments('configure_timing_sample_clock', options)
    print 'configure_timing_sample_clock', kws
    clock_rate = kws.get('rate', 1000.0)
    task.configure_timing_sample_clock(**kws)
    print 'task'
    task.start()
    args, read_kws = get_method_arguments('ai_read', options)
    kws = read_kws
    fill_mode = kws.get ('fill_mode', 'group_by_scan_number')
    print 'read', read_kws

    if options.ai_task=='show':
        from nidaqmx.wxagg_plot import animated_plot
        start_time = time.time()
        def func(task=task):
            current_time = time.time()
            data = task.read(**read_kws)
            if fill_mode == 'group_by_scan_number':
                data = data.T
            tm = np.arange(data.shape[-1], dtype=float)/clock_rate + (current_time - start_time)
            return tm, data, channels
        try:
            animated_plot(func, 1000*(task.samples_per_channel/clock_rate+0.1))
        finally:
            del task
        return
    elif options.ai_task=='print':
        try:
            data = task.read (**kws)
        finally:
            del task
        print data
    else:
        del task
        raise NotImplementedError (`options.ai_task`)

def main ():
    parser = OptionParser()
    set_ai_options(parser)
    if hasattr(parser, 'runner'):
        parser.runner = runner
    options, args = parser.parse_args()
    runner(parser, options, args)
    return

if __name__=="__main__":
    main()

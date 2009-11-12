#!/usr/bin/env python
# -*- python-mode -*-
"""
"""
# Author: Pearu Peterson
# Created: August 2009

from __future__ import division
import os
import sys

### START UPDATE SYS.PATH ###
### END UPDATE SYS.PATH ###

import numpy as np

from ioc.optparse_gui import OptionParser
from optparse import OptionGroup

from nidaqmx import AnalogInputTask
from nidaqmx.optparse_options import get_method_arguments, set_ai_options

def runner (parser, options, args):
    task = AnalogInputTask()
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
    args, kws = get_method_arguments('ai_read', options)
    fill_mode = kws.get ('fill_mode', 'group_by_scan_number')
    print 'read', kws
    try:
        data = task.read (**kws)
    except KeyboardInterrupt:
        print 'Caught Ctrl-C.'
        del task
        return
    del task

    if fill_mode == 'group_by_scan_number':
        data = data.T

    if options.ai_task=='print':
        print data
    elif options.ai_task=='plot':
        from matplotlib import pyplot as plt
        def on_keypressed(event):
            key = event.key
            if key=='q':
                sys.exit(0)
        fig = plt.figure(1, figsize=(12,6))
        fig.canvas.mpl_connect('key_press_event', on_keypressed)
        tm = np.arange(data.shape[-1], dtype=float)/clock_rate
        for index in range(len(channels)):
            plt.plot(tm, data[index])
        plt.legend(channels)
        plt.xlabel('Seconds')
        plt.ylabel('Volts')
        plt.title('nof samples=%s' % (len(tm)))
        plt.draw()
        plt.show()
    else:
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

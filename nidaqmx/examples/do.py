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

from nidaqmx import DigitalOutputTask
from nidaqmx.optparse_options import get_method_arguments, set_do_options

def runner (parser, options, args):
    task = DigitalOutputTask()

    print 'Created DigitalOutputTask %s (task.value=%s)' % (task, task.value)

    args, kws = get_method_arguments('create_channel', options)
    print 'create_channel', kws
    task.create_channel (**kws)

    channels = task.get_names_of_channels()
    if not channels:
        print 'No channels specified'
        return

    args, kws = get_method_arguments('ao_write', options)
    layout = kws.get('layout', 'group_by_scan_number')

    if not options.do_write_auto_start:
        task.start()

    if options.do_task=='tenfive':
        try:
            for n in range(options.do_task_duration):
                if n%2:
                    data = np.array([1,0,1,0], dtype=np.uint8)
                else:
                    data = np.array([0,1,0,1], dtype=np.uint8)
                task.write (data.ravel (), **kws)
                time.sleep(1)
        except KeyboardInterrupt:
            print 'Caught Ctrl-C.'
        task.stop ()
        del task
        return

    if options.do_task=='scalar0':
        data = np.uint8(0)
    elif options.do_task=='scalar1':
        data = np.uint8(1)
    elif options.do_task=='ten': # 1010
        data = np.array([1,0,1,0], dtype=np.uint8)
    else:
        raise `options.do_task`

    if layout=='group_by_scan_number':
        data = data.T

    print 'samples available/written per channel= %s/%s ' % (data.size//len(channels), task.write(data.ravel(), **kws))

    try:
        time.sleep (options.do_task_duration)
    except KeyboardInterrupt:
        print 'Caught Ctrl-C.'

    task.stop ()
    del task

def main ():
    parser = OptionParser()
    set_do_options(parser)
    if hasattr(parser, 'runner'):
        parser.runner = runner
    options, args = parser.parse_args()
    runner(parser, options, args)
    return

if __name__=="__main__":
    main()

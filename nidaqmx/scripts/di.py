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

from nidaqmx import DigitalInputTask
from nidaqmx.optparse_options import get_method_arguments, set_di_options

def runner (parser, options, args):
    task = DigitalInputTask()

    print 'Created DigitalInputTask %s (task.value=%s)' % (task, task.value)

    args, kws = get_method_arguments('create_channel', options)
    print 'create_channel', kws
    task.create_channel (**kws)

    channels = task.get_names_of_channels()
    if not channels:
        print 'No channels specified'
        return

    print 'task start'
    task.start()
    args, read_kws = get_method_arguments('di_read', options)
    kws = read_kws
    fill_mode = kws.get ('fill_mode', 'group_by_scan_number')
    print 'read', read_kws

    if options.di_task=='print':
        try:
            data, bytes_per_sample = task.read (**kws)
        finally:
            del task
        print bytes_per_sample
        print data
    else:
        del task
        raise NotImplementedError (`options.di_task`)

def main ():
    parser = OptionParser()
    set_di_options(parser)
    if hasattr(parser, 'runner'):
        parser.runner = runner
    options, args = parser.parse_args()
    runner(parser, options, args)
    return

if __name__=="__main__":
    main()

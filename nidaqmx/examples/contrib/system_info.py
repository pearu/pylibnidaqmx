"""
Use pylibnidaqmx to discover information aobut the National Instruments NI-DAQ devices on the system
useful to know what to call the terminal strings
May be able to expand to make a database of the hardware capabilities

"""

from pprint import pprint,pformat
import os
import sys
import nidaqmx


class NidaqInfo(object):
    """
    describe the current computer's NI-DAQ devices and interfaces
    """
    def __init__(self,logfile='hardware_info.log'):
        if not hasattr(logfile,'write'):
            # assume it's a string
            self.log = open(logfile, 'wb+')
        else:
            self.log = logfile
        self.system = nidaqmx.libnidaqmx.System()
        title1="NI-DAQmx system info"
        self.both('='*len(title1),'\n')
        self.both(title1,"\n")
        self.both('='*len(title1),'\n')
        self.both("system platform:", sys.platform,"\n")
        ss = self.system
        self.both("NI-DAQ version %d.%d\n" %( ss.major_version, ss.minor_version))
        self.devices = ss.devices
        self.both("devices:", self.devices,"\n")
        self.tasks = ss.tasks
        self.both("current tasks:", self.tasks, "\n")
        self.global_channels= ss.global_channels
        self.both("global channels:", self.global_channels, "\n")

        for dd in self.devices:
            self.print_dev_info(dd)
             

    def both(self, *args):
        a = [str(x) for x in args]
        s = " ".join(a)
        print s,
        print >>self.log, s,

    def bothnl(self):
        print
        print >>self.log,""
        

    def print_dev_info(self, dvstr='Dev1'):
        self.device = nidaqmx.libnidaqmx.Device(dvstr)
        device = self.device
        title = "For device: %s" % dvstr
        self.both(title,"\n")
        self.both("-"*len(title),"\n")
        self.both("device product type:", device.get_product_type(),"\n")
        self.both("product number:", device.get_product_number(), "\n")
        self.both("bus type:", device.get_bus_type(),"\n")
        self.both("counter output channels:", device.get_counter_output_channels(),"\n")
        self.both("counter input channels", device.get_counter_input_channels(),"\n")
        self.both("digital output ports:", device.get_digital_output_ports(),"\n")
        self.both("digital input ports:", device.get_digital_input_ports(),"\n")
        self.both("analog outputs:", device.get_analog_output_channels(),"\n")
        self.both("analog inputs:", device.get_analog_input_channels(),"\n")
 
       # detailed stuff to file, not screen
        print >>self.log, "get_digital_output_lines:", "counter output channels:", device.get_counter_output_channels()
        print >>self.log, "counter input channels", device.get_counter_input_channels()
        print >> self.log, "get_digital_output_lines:", pformat(device.get_digital_output_lines())
        print >>self.log, "get_digital_output_ports:",
        print >> self.log, pformat(device.get_digital_output_ports())

def main():
    print "Getting NI-DAQmx info, printing to screen and logging details to hardware_info.log"
    info = NidaqInfo()
    

if __name__=='__main__':
    main()

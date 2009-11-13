
import os
from optparse import OptionGroup

def get_method_arguments(methodname, options, kws=None):
    args = []
    if kws is None:
        kws = {}
    for name in dir (options):
        value = getattr (options, name)
        if name.startswith(methodname) and value is not None:
            kws[name[len(methodname)+1:]] = value
    return tuple(args), kws

def set_di_options (parser):
    if os.name == 'posix':
        parser.run_methods = ['subcommand']

    import nidaqmx
    from nidaqmx.libnidaqmx import make_pattern
    parser.set_usage ('''\
%prog [options]

Description:
  %prog provides graphical interface to NIDAQmx digital input task.
''')
    phys_channel_choices = []
    for dev in nidaqmx.DigitalInputTask.get_system_devices():
        phys_channel_choices.extend(dev.get_digital_input_lines())
    pattern = make_pattern(phys_channel_choices)
    parser.add_option ('--create-channel-lines',
                       type = 'string',
                       help = 'Specify digital lines as a pattern ['+pattern+']. Default: %default.')
    get_digital_io_options_group (parser, parser)
    get_di_read_options_group (parser, parser)
    parser.add_option('--di-task',
                      default = 'print',
                      choices = ['print'])

def set_ai_options (parser):
    if os.name == 'posix':
        parser.run_methods = ['subcommand']

    import nidaqmx
    from nidaqmx.libnidaqmx import make_pattern
    parser.set_usage ('''\
%prog [options]

Description:
  %prog provides graphical interface to NIDAQmx analog input task.
''')
    ai_phys_channel_choices = []
    for dev in nidaqmx.AnalogInputTask.get_system_devices():
        ai_phys_channel_choices.extend(dev.get_analog_input_channels())
    pattern = make_pattern(ai_phys_channel_choices)
    parser.add_option ('--create-voltage-channel-phys-channel',
                       type = 'string',
                       help = 'Specify physical channel as a pattern ['+pattern+']. Default: %default.')
    get_analog_io_options_group (parser, parser)
    get_ai_read_options_group (parser, parser)
    parser.add_option('--ai-task',
                      default = 'print',
                      choices = ['print', 'plot', 'show'])
    parser.add_option_group (get_configure_timing_options_group (parser))

def set_ao_options (parser):
    if os.name == 'posix':
        parser.run_methods = ['subcommand']

    import nidaqmx
    from nidaqmx.libnidaqmx import make_pattern

    parser.set_usage ('''\
%prog [options]

Description:
  %prog provides graphical interface to NIDAQmx analog output task.
''')
    ao_phys_channel_choices = []
    for dev in nidaqmx.AnalogOutputTask.get_system_devices():
        ao_phys_channel_choices.extend(dev.get_analog_output_channels())
    pattern = make_pattern(ao_phys_channel_choices)
    parser.add_option ('--create-voltage-channel-phys-channel',
                       type = 'string',
                       help = 'Specify physical channel as a pattern ['+pattern+']. Default: %default.')
    get_analog_io_options_group(parser, parser, skip_terminal=True)
    get_ao_write_options_group (parser, parser)

    parser.add_option('--ao-task',
                      default = 'sin',
                      choices = ['sin'])
    parser.add_option ('--ao-task-duration',
                       type = 'float',
                       default = 10.0)
    parser.add_option_group (get_configure_timing_options_group (parser))

def get_configure_timing_options_group(parser, group=None):
    if group is None:
         group = OptionGroup(parser, 'Timing options')
    group.add_option ('--configure-timing-sample-clock-source',
                       type = 'string', default='OnboardClock',
                       )
    group.add_option ('--configure-timing-sample-clock-rate',
                      default = 1.0,
                      type = 'float',
                      )
    group.add_option ('--configure-timing-sample-clock-active-edge',
                       choices = ['rising','falling'],
                       )
    group.add_option ('--configure-timing-sample-clock-sample-mode',
                      default = 'continuous',
                       choices = ['finite','continuous','hwtimed'])

    group.add_option ('--configure-timing-sample-clock-samples-per-channel',
                      type = 'int'
                      )
    return group

def get_analog_io_options_group (parser, group=None, skip_terminal=False):
    if group is None:
        group = OptionGroup (parser, 'Analog I/O options')

    group.add_option ('--create-voltage-channel-channel-name',
                      type = 'string')
    if not skip_terminal:
        group.add_option ('--create-voltage-channel-terminal',
                          choices = ['default','rse','nrse','diff','pseudodiff'])
    group.add_option ('--create-voltage-channel-min-val',
                      type = 'float')
    group.add_option ('--create-voltage-channel-max-val',
                      type = 'float',
                      )
    group.add_option ('--create-voltage-channel-units',
                      choices = ['volts', 'custom'])
    group.add_option ('--create-voltage-channel-custom-scale-name')

    return group

def get_digital_io_options_group (parser, group=None):
    if group is None:
        group = OptionGroup (parser, 'Digital I/O options')

    group.add_option ('--create-channel-name',
                      type = 'string')
    group.add_option ('--create-channel-grouping',
                      choices = ['per_line', 'for_all_lines']
                      )
    return group


def get_ai_read_options_group(parser, group=None):
    assert group is not None, `group`
    group.add_option ('--ai-read-samples-per-channel',
                      type = 'int')
    group.add_option ('--ai-read-timeout',
                      default = 10.0,
                      type = 'float')
    group.add_option ('--ai-read-fill-mode',
                      choices = ['group_by_scan_number','group_by_channel'])

    return group

def get_di_read_options_group(parser, group=None):
    assert group is not None, `group`
    group.add_option ('--di-read-samples-per-channel',
                      type = 'int')
    group.add_option ('--di-read-timeout',
                      default = 10.0,
                      type = 'float')
    group.add_option ('--di-read-fill-mode',
                      choices = ['group_by_scan_number','group_by_channel'])

    return group

def get_ao_write_options_group(parser, group=None):
    assert group is not None, `group`
    group.add_option ('--ao-write-auto-start', action='store_true')
    group.add_option ('--no-ao-write-auto-start', dest='ao_write_auto_start', action='store_false')
    group.add_option ('--ao-write-timeout',
                      default = 10.0,
                      type = 'float')
    group.add_option ('--ao-write-layout',
                      choices = ['group_by_scan_number','group_by_channel'])

    return group

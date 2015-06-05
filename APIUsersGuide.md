# Overview #

See also auto-generated [API documentation of nidaqmx](http://pylibnidaqmx.googlecode.com/svn/trunk/apidocs/index.html).

The `nidaqmx` Python package provides 6 classes to create
NIDAQmx tasks:

  * AnalogInputTask
  * AnalogOutputTask
  * DigitalInputTask
  * DigitalOutputTask
  * CounterInputTask
  * CounterOutputTask

The base class for these classes is `Task` that implements the following methods:

State related methods:
  * start()
  * stop()
  * is\_done()
  * alter\_state(state=start|stop|verify|commit|reserve|unreserve|abort)
  * wait\_until\_done(timeout=-1)

Defining callback methods:
  * register\_every\_n\_samples\_event(func,samples=1,options=0|sync,cb\_data=None)
  * register\_done\_event(func,options=,cb\_data=)
  * register\_signal\_event(func,signal=sample\_clock|sample\_complete|change\_detection|counter\_output,options=,cb\_data)

Timing methods:
  * configure\_timing\_handchaking(sample\_mode=,samples\_per\_channel=)
  * configure\_timing\_implicit(sample\_mode=,samples\_per\_channel=)
  * configure\_timing\_change\_detection(rising\_edge\_channel=,falling\_edge\_channel=,sample\_mode=,samples\_per\_channel=)
  * configure\_timing\_sample\_clock(source=OnboardClock,rate=1,active\_edge=rising|falling,sample\_mode=finite|continuous|hwtimed,samples\_per\_channel=)

Triggering methods:
  * configure\_trigger\_analog\_edge\_start(source, slope=rising|falling,level=)
  * configure\_trigger\_analog\_window\_start(source, when=entering|leaving,top=,bottom=)
  * configure\_trigger\_digital\_edge\_start(source, edge=rising|falling)
  * configure\_trigger\_digital\_pattern\_start(source, pattern, when=matches|does\_not\_match)
  * configure\_trigger\_disable\_start()

Various setter/getter/resetter methods:
  * set\_buffer(samples\_per\_channel)
  * set/get/reset\_buffer\_size(sz//)
  * set/get/reset\_max(channel\_name,value//)
  * set/get/reset\_min(channel\_name,value//)
  * get\_low/high/gain/measurement\_type/units/auto\_zero\_mode/data\_transfer\_mechanism(channel\_name)
  * set/get/reset\_regeneration(bool//)
  * set/get/reset\_arm\_start\_trigger(trigger\_type=digital\_edge//)

  * set\_arm\_start\_trigger\_source(source)
  * set\_arm\_start\_trigger\_edge(edge=rising|falling)

  * set\_pause\_trigger(trigger\_type=analog\_level|analog\_window|digital\_level)
  * set\_pause\_trigger\_source(source)
  * set\_pause\_trigger\_when(when=above|below|inside|outside|high|low)

AnalogInput/OutputTask methods:
  * create\_voltage\_channel(phys\_channel,channel\_name=,terminal=default|rse|nrse|diff|pseudodiff,min\_val=,max\_val=,units=volts|custom,custom\_scale\_name=)
  * read(samples\_per\_channel=,timeout=10,fill\_mode=group\_by\_scan\_number|group\_by\_channel) -> data
  * write(data, auto\_start=True,timeout=10,layout=group\_by\_scan\_number|group\_by\_channel)

DigitalInput/OutputTask methods:
  * create\_channel(lines, name=, grouping=per\_line|for\_all\_lines)
  * read(samples\_per\_channel=,timeout=10,fill\_mode=group\_by\_scan\_number|group\_by\_channel) -> data, bytes\_per\_sample
  * write(data,auto\_start=True,timeout=10,layout=group\_by\_scan\_number|group\_by\_channel)

CounterInput/OutputTask methods:
  * create\_channel\_count\_edges(counter,name=,edge=rising|falling,init=0,direction=up|down|ext)
  * set\_terminal\_count\_edges(channel, terminal)
  * create\_channel\_frequency(counter,name=,units=hertz,idle\_state=low|high,delay=0,freq=1,duty\_cycle=0.5)
  * create\_channel\_ticks(counter,name=,source=,idle\_state=low|high,delay=0,low\_ticks=1,high\_ticks=1)
  * create\_channel\_time(counter,name=,units=seconds,idle\_state=low|high,delay=0,low\_time=1,high\_time=1)
  * set\_terminal\_pulse(channel, terminal)
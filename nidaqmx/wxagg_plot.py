
import os
import sys
import time
import traceback
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

import wx

from matplotlib.figure import Figure

class PlotFigure(wx.Frame):

    def OnKeyPressed (self, event):
        key = event.key
        if key=='q':        
            self.OnClose(event)

    def __init__(self, func, timer_period):
        wx.Frame.__init__(self, None, -1, "Plot Figure")

        self.fig = Figure((12,9), 75)
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.canvas.mpl_connect('key_press_event', self.OnKeyPressed)
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        self.func = func
        self.plot = None

        self.timer_period = timer_period
        self.timer = wx.Timer(self)
        self.is_stopped = False

        if os.name=='nt':
            # On Windows, default frame size behaviour is incorrect
            # you don't need this under Linux
            tw, th = self.toolbar.GetSizeTuple()
            fw, fh = self.canvas.GetSizeTuple()
            self.toolbar.SetSize(Size(fw, th))

        # Create a figure manager to manage things

        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(self.canvas, 1, wx.LEFT|wx.TOP|wx.GROW)
        # Best to allow the toolbar to resize!
        sizer.Add(self.toolbar, 0, wx.GROW)
        self.SetSizer(sizer)
        self.Fit()
        self.Bind(wx.EVT_TIMER, self.OnTimerWrap, self.timer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.timer.Start(timer_period)

    def GetToolBar(self):
        # You will need to override GetToolBar if you are using an
        # unmanaged toolbar in your frame
        return self.toolbar

    def OnClose(self, event):
        self.is_stopped = True
        print 'Closing PlotFigure, please wait.'
        self.timer.Stop()
        self.Destroy()

    def OnTimerWrap (self, evt):
        if self.is_stopped:
            print 'Ignoring timer callback'
            return
        t = time.time()
        try:
            self.OnTimer (evt)
        except KeyboardInterrupt:
            self.OnClose(evt)
        duration = 1000*(time.time () - t)
        if duration > self.timer_period:
            print 'Changing timer_period from %s to %s msec' % (self.timer_period, 1.2*duration)
            self.timer_period = 1.2*duration
            self.timer.Stop()
            self.timer.Start (self.timer_period)

    def OnTimer(self, evt):

        try:
            xdata, ydata_list, legend = self.func()
        except RuntimeError:
            traceback.print_exc(file=sys.stderr)
            self.OnClose(evt)
            return
        if len (ydata_list.shape)==1:
            ydata_list = ydata_list.reshape((1, ydata_list.size))
        if self.plot is None:
            self.axes = self.fig.add_axes([0.1,0.1,0.8,0.8])
            l = []
            for ydata in ydata_list:
                l.extend ([xdata, ydata])
            self.plot = self.axes.plot(*l)
            self.axes.set_xlabel('Seconds')
            self.axes.set_ylabel('Volts')
            self.axes.set_title('nof samples=%s' % (len(xdata)))
            self.axes.legend (legend)
        else:
            self.axes.set_xlim(xmin = xdata[0], xmax=xdata[-1])
            ymin, ymax = 1e9,-1e9
            for line, data in zip (self.plot, ydata_list):
                line.set_xdata(xdata)
                line.set_ydata(data)
                ymin, ymax = min (data.min (), ymin), max (data.max (), ymax)
            dy = (ymax-ymin)/20
            self.axes.set_ylim(ymin=ymin-dy, ymax=ymax+dy)
        self.canvas.draw()

    def onEraseBackground(self, evt):
        # this is supposed to prevent redraw flicker on some X servers...
        pass

def animated_plot(func, timer_period):
    app = wx.PySimpleApp(clearSigInt=False)
    frame = PlotFigure(func, timer_period)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    from numpy import *
    import time
    start_time = time.time ()
    def func():
        x = arange (100, dtype=float)/100*pi
        d = sin (x+(time.time ()-start_time))
        return x, d, ['sin (x+time)']

    try:
        animated_plot (func, 1)
    except Exception, msg:
        print 'Got exception: %s' % ( msg)
    else:
        print 'Exited normally'

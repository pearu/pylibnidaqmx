"""
Simple class to represent a constants container.

The container is actually a dictionary, but items can be accessed as properties,
rather than only by indexing the dictionary (e.g. D['i']).

This container does not allow items to be changed via typical __setitem__ or
__setattr__ methods:
  D['i'] = 1 # raises an error
  D.i = 1 # raises an error

Using this class as the container for constants rather than a namedtuple removes
the limitation of 255 items allowed in the collection for all versions of
Python.
"""

class DAQmxConstants(dict):
    def __init__(self, *a, **kw):
        super(DAQmxConstants, self).__init__(*a, **kw)
        super(DAQmxConstants, self).__setattr__('__dict__', self)
    def __setitem__(self, i, v):
        raise NotImplemented('Cannot change item')
    def __setattr__(self, i, v):
        raise NotImplemented('Cannot change item')


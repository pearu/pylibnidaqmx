def customtuple(*keys):
    """
    Create a namedtuple that can handle more than 255 elements (in python 3)

    Source:
    http://stackoverflow.com/questions/18550270/any-way-to-bypass-namedtuple-255-arguments-limitation/18550314
    """
    class string:
        _keys = keys
        _dict = {}
        def __init__(self, *args):
            args = list(args)
            if len(args) != len(self._keys):
                raise Exception("No go forward")

            for key in range(len(args)):
                self._dict[self._keys[key]] = args[key]

        def __setattr__(self, *args):
            raise BaseException("Not allowed")

        def __getattr__(self, arg):
            try:
                return self._dict[arg]
            except:
                raise BaseException("Name not defined")

        def __repr__(self):
            return ("string(%s)"
                    %(", ".join(["%s=%r"
                                 %(self._keys[key],
                                   self._dict[self._keys[key]])
                                 for key in range(len(self._dict))])))

    return string
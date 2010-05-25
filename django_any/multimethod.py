#-*- coding: utf-8 -*-
__registry = {}


class MultiMethod(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}
    def __call__(self, *args, **kwargs):
        types = tuple(arg.__class__ for arg in args)
        function = self.typemap.get(types)
        if function is None:
            raise TypeError("no match %s" % types)
        return function(*args, **kwargs)
    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function


def multimethod(*types):
    """
    Decorator for multimethod registration

    >>> @multimethod(int)
    ... def test(an_int):
    ...     print "INT"
    >>> @multimethod(str)
    ... def test(a_str):
    ...     print "STRING"
    >>> test(0)
    INT
    >>> test('')
    STRING
    """
    def register(function):
        name = function.__name__
        mm = __registry.get(name)
        if mm is None:
            mm = __registry[name] = MultiMethod(name)
        mm.register(types, function)
        return mm
    return register


if __name__ == "__main__":
    import doctest
    doctest.testmod()

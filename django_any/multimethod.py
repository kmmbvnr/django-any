#-*- coding: utf-8 -*-
__registry = {}

class MultiMethod(object):
    """
    Multimetod dispatcher
    """
    def __init__(self, name, module):
        self.name = name
        self.typemap = {}

        # replacer for real functions, doctest accomulator
        self.caller = lambda *args, **kwargs: self.__call__(*args, **kwargs)
        self.caller.__module__ = module
        self.caller.__doc__ = self.__doc__

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
        if function.__doc__:
            self.caller.__doc__ += function.__doc__

    def register_decorator(self, decorator):
        self.__call__ = decorator(self.__call__)
        self.caller.__doc__ += (decorator.__doc__ or "")


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
            mm = __registry[name] = MultiMethod(name, function.__module__)
        mm.register(types, function)
        return mm.caller
    return register


def multimethod_decorator(function):
    """
    Decorator for multimetod decorators registration

    >>> @multimethod_decorator
    ... def test_decorated(function):
    ...      def wrapper(*args, **kwargs):
    ...           print "BEFORE"
    ...           result = function(*args, **kwargs)
    ...           print "AFTER"
    ...           return result
    ...      return wrapper
    >>> @multimethod(int)
    ... def test_decorated(an_int):
    ...     print "INT"
    >>> @multimethod(str)
    ... def test_decorated(a_str):
    ...     print "STRING"
    >>> test_decorated(0)
    BEFORE
    INT
    AFTER
    >>> test_decorated('')
    BEFORE
    STRING
    AFTER
    """
    name = function.__name__
    mm = __registry.get(name)
    if mm is None:
        mm = __registry[name] = MultiMethod(name, function.__module__)
    mm.register_decorator(function)
    return mm.caller


if __name__ == "__main__":
    import doctest
    doctest.testmod()

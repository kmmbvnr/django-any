#-*- coding: utf-8 -*-
__registry = {}

class MultiMethod(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}
        self.decorators = []

    def __call__(self, *args, **kwargs):
        types = tuple(arg.__class__ for arg in args)
        function = self.typemap.get(types)

        if function is None:
            raise TypeError("no match %s" % types)

        for decorator in self.decorators:
            function = decorator(function)

        return function(*args, **kwargs)

    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function

    def register_decorator(self, decorator):
        self.decorators.append(decorator)


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
        mm = __registry[name] = MultiMethod(name)
    mm.register_decorator(function)
    return mm


if __name__ == "__main__":
    import doctest
    doctest.testmod()

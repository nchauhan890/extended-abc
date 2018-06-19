# abstractmethod decorator for extended-abc

from functools import wraps


def abstractmethod(f):
    """Function decorator which sets the abstract attribute of a function to True.

    Can also be set directly after the function definition with:

        function.abstract = True
        or... function = abstractmethod(function)


    Should be used within classes whose metaclass is Abstract
    to indicate that a method is abstract and must therefore be
    derived from.

    Usage:

    class AbstractClass(metaclass=Abstract):

        @abstractmethod
        def foo(self):
            pass

        # or...

        def bar(self):
            pass
        bar.abstract = True

        # or...

        def baz(self):
            pass
        baz = abstractmethod(baz)

    """
    @wraps(f)
    def inner(*args, **kwargs):
        return
    f.abstract = True
    return f

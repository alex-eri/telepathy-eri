__author__ = 'eri'
import gobject
def decorator(function):
    """decorator to be used on decorators, it preserves the docstring and
    function attributes of functions to which it is applied."""
    def new_decorator(f):
        g = function(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    new_decorator.__name__ = function.__name__
    new_decorator.__doc__ = function.__doc__
    new_decorator.__dict__.update(function.__dict__)
    return new_decorator

@decorator
def async(func):
    """Make a function mainloop friendly. the function will be called at the
    next mainloop idle state."""
    def new_function(*args, **kwargs):
        def async_function():
            func(*args, **kwargs)
            return False
        gobject.idle_add(async_function)
    return new_function


import logging
logger = logging.getLogger('Eri.Decorators')


def loggit(logger=logger,lm='lambda'):
    @decorator
    def outer(f):
        def inner(*args,**kwargs):
            logger.debug('Calling {} {}:'.format(f.__name__.replace('lambda',lm), repr(args)))
            logger.debug(repr(kwargs))
            try:
                ret = f(*args,**kwargs)
            except Exception,e:
                logger.error('{}: {}'.format(e.__class__.__name__, e.message))
                raise e
            logger.debug(repr(ret))
            return ret
        return inner
    return outer
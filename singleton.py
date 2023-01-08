#!/usr/bin/env python
__author__ = "Joe Abdo"
__copyright__ = "Copyright 2023s"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "joe-abdo3@hotmail.com"
__status__ = "Production"

def singleton(class_):
    """Decorator used to make all the classes it is applied to,
            singleton classes.

    Parameters
    ----------
    class_ : Class
        targeted class to be made singleton
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance

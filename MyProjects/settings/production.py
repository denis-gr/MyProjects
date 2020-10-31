from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

try:
    from .secret import *
except ImportError:
    pass

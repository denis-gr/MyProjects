from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass

try:
    from .secret import *
except ImportError:
    pass

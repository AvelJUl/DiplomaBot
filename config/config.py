TOKEN = None

DEFAULT_LANGUAGE = None

try:
    from .local_config import *
except ImportError:
    pass

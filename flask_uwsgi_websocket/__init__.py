'''
Flask-uWSGI-WebSocket
---------------------
High-performance WebSockets for your Flask apps powered by `uWSGI <http://uwsgi-docs.readthedocs.org/en/latest/>`_.
'''

__docformat__ = 'restructuredtext'
__version__ = '0.1.5'
__license__ = 'MIT'
__author__ = 'Zach Kelling'

from .websockets import *
from .async import *
try:
    from .gevent import *
except ImportError:
    pass

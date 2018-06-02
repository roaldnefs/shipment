"""
Shipment package for Python.
"""

import logging
from logging import NullHandler

from shipment.formatters import LogstashFormatter
from shipment.handlers import RedisHandler, LogstashHandler

__author__ = "Roald Nefs <info@roaldnefs.com>"
__status__ = "development"
__version__ = "0.0.1"


logging.getLogger(__name__).addHandler(NullHandler())

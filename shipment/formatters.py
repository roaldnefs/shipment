import logging
import socket
import sys
import traceback
from datetime import datetime
try:
    import json
except ImportError:
    import simplejson as json


class LogstashFormatter(logging.Formatter):
    """
    Logging formatter for Logstash.

    Based on Volodymyr Klochan's LogstashFormatterVersion1.
    """
    def __init__(self, message_type='Logstash', tags=None, fqdn=False):
        self.message_type = message_type
        self.tags = tags if tags is not None else []

        if fqdn:
            self.host = socket.getfdqn()
        else:
            self.host = socket.gethostname()

    def get_extra_fields(self, record):
        # The list contains all the attributes listed in:
        # http://docs.python.org/library/logging.html#logrecord-attributes
        skip_list = (
            'args', 'asctime', 'created', 'exc_info', 'filename', 'funcName',
            'levelname', 'levelno', 'lineno', 'message', 'module', 'msecs',
            'msg', 'name', 'pathname', 'process', 'processName',
            'relativeCreated', 'stack_info', 'thread', 'threadName')

        if sys.version_info < (3, 0):
            easy_types = (basestring, bool, dict, float, int, long, list, type(None))
        else:
            easy_types = (str, bool, dict, float, int, list, type(None))

        fields = {}

        for key, value in record.__dict__.items():
            if key not in skip_list:
                if isinstance(value, easy_types):
                    fields[key] = value
                else:
                    fields[key] = repr(value)

        return fields

    def get_debug_fields(self, record):
        fields = {
            'stack_trace': self.format_exception(record.exc_info),
            'lineno': record.lineno,
            'process': record.process,
            'thread_name': record.threadName,
            'funcName': record.funcName,
            'processName': record.processName,
        }

        return fields

    @classmethod
    def format_source(cls, message_type, host, path):
        return "{}://{}/{}".format(message_type, host, path)

    @classmethod
    def format_timestamp(cls, time):
        timestamp = datetime.utcfromtimestamp(time)
        return "{}.{:03}Z".format(
            timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
            (timestamp.microsecond / 1000)
        )

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    @classmethod
    def serialize(cls, message):
        if sys.version_info < (3, 0):
            return json.dumps(message)
        else:
            return bytes(json.dumps(message), 'utf-8')

    def format(self, record):
        # Create message dict
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,
            'path': record.pathname,
            'tags': self.tags,
            'type': self.message_type,

            # Extra Fields
            'level': record.levelname,
            'logger_name': record.name,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)

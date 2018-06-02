import logging
from logging.handlers import SocketHandler
import redis

from shipment.utils import import_from_string
from shipment.formatters import RedisFormatter, LogstashFormatter


class RedisHandler(logging.Handler):
    """
    Publish messages to Redis channel.

    As a convenience, the classmethod to() can be used as a
    constructor, just as in Andrei Savu's mongodb-log handler.

    Based on Jed Parsons' RedisHandler.
    """

    @classmethod
    def to(cklass, channel, host='localhost', port=6379, password=None, level=logging.NOTSET):
        return cklass(channel, redis.Redis(host=host, port=port, password=password), level=level)

    def __init__(self, channel, redis_client, level=logging.NOTSET):
        """
        Create a new logger for the given channel and redis_client.
        """
        logging.Handler.__init__(self, level)
        self.channel = channel
        self.redis_client = redis_client
        self.formatter = LogstashFormatter()

    def emit(self, record):
        """
        Publish record to Redis logging channel.
        """
        try:
            self.redis_client.publish(self.channel, self.format(record))
        except redis.RedisError:
            pass


class LogstashHandler(SocketHandler):
    """
    Python logging handler for Logstash.

    Sends events over TCP.

    Based on Volodymyr Klochan's TCPLogstashHandler.
    """
    def __init__(self, host='localhost', port=5959, formatter='shipment.LogstashFormatter', message_type='logstash', tags=None, fqdn=False):
        super(LogstashHandler, self).__init__(host, port)

        # Import formatter class.
        klass = import_from_string(formatter)

        if formatter in ('shipment.LogstashFormatter', 'shipment.formatters.LogstashFormatter'):
            self.formatter = klass(message_type, tags, fqdn)
        else:
            self.formatter = klass()

    def makePickle(self, record):
        return self.formatter.format(record) + b'\n'

import logging
import shipment
import sys


host = 'localhost'

# Configure the logger and add a Logstash and Redis handler.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.addHandler(shipment.LogstashHandler(host, 5959))
logger.addHandler(shipment.RedisHandler.to('redis_test', host='localhost', port=6379, level=logging.DEBUG))

# Send some logs.
logger.error('test logstash error message.')
logger.info('test logstash info message.')
logger.warning('test logstash warning message.')

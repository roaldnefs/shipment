import logging
import shipment


host = 'localhost'

# Configure the logger and add a Logstash and Redis handler.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(shipment.LogstashHandler(host, 5959))
logger.addHandler(shipment.RedisHandler('redis_test', host=host, port=6379, level=logging.DEBUG))

# Send some logs.
logger.error('test logstash error message.')
logger.info('test logstash info message.')
logger.warning('test logstash warning message.')

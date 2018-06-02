# Shipment

Ship Python logging to your ELK Stack.

## Installation

Using pip:

```bash
pip install shipment
```

## Usage

For example:

```python
import logging
import shipment


host = 'localhost'

# Configure the logger and add a Logstash and Redis handler.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.addHandler(shipment.LogstashHandler(host, 5959))
logger.addHandler(shipment.RedisHandler('redis_test', host=host, port=6379, level=logging.DEBUG))

# Send some logs.
logger.error('test logstash error message.')
logger.info('test logstash info message.')
logger.warning('test logstash warning message.')
```

## Using with Django

Modify your `settings.py` to integrate `shipment` with Django's logging:

```python
LOGGING = {
  ...
  'handlers': {
      'logstash': {
          'level': 'DEBUG',
          'class': 'shipment.LogstashHandler',
          'host': 'localhost',
          'port': 5959, # Default value: 5959.
          'formatter': 'shipment.LogstashFormatter', # Default value: 'shipment.LogstashFormatter'.
          'message_type': 'logstash',  # 'type' field in logstash message. Default value: 'logstash'.
          'fqdn': False, # Fully qualified domain name. Default value: False.
          'tags': ['tag1', 'tag2'], # list of tags. Default: None.
      },
      'redis': {
          'level': 'DEBUG',
          'class': 'shipment.RedisHandler',
          'host': 'localhost',
          'port': 6379, # Default value: 6379.
          'password': None, # Default value: None.
          'formatter': 'shipment.LogstashFormatter', # Default value: 'shipment.LogstashFormatter'.
          'message_type': 'redis', # 'type' field in logstash message. Default value: 'logstash'.
          'fqdn': False, # Fully qualified domain name. Default value: False.
          'tags': ['tag1', 'tag2'], # List of tags. Default: None.
      },
  },
  'loggers': {
      'django.request': {
          'handlers': ['logstash', 'redis'],
          'level': 'DEBUG',
          'propagate': True,
      },
  },
  ...
}
```

## Example Logstash Configuration

Example Logstash configuration (`logstash.conf`) for receiving evens from `shipment`:

```bash
input {
  tcp {
    port  => 5959
    codec => json
  }
  redis {
    host      => 'redis'
    port      => 6379
    data_type => 'channel'
    key       => 'redis_test'
  }
}
```

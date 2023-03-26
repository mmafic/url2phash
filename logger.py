import os
import logging

logging.basicConfig()
logger = logging.getLogger()

if 'DEBUG' in os.environ:
  logger.setLevel(logging.DEBUG)
  logger.debug('Running in DEBUG mode')
else:
  logger.setLevel(logging.INFO)
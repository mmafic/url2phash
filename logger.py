import os
import logging

logging.basicConfig()
logger = logging.getLogger()

if 'DEBUG' in os.environ:
  logger.setLevel(logging.DEBUG)
else:
  logger.setLevel(logging.INFO)
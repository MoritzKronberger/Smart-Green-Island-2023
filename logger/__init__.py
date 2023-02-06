"""Handle app-wide logging."""
import logging

__logger_name = 'default'

# Create app logger
# Derived from:
# https://docs.python.org/3/howto/logging.html#configuring-logging
logger = logging.getLogger(__logger_name)

# Set log-level to debug
logger.setLevel(logging.DEBUG)

# Create console handler and formatter
__handler = logging.StreamHandler()
# Set formatter format as 'time - loglevel - message'
__formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# Add formatter to handler
__handler.setFormatter(__formatter)
# Add handler to logger
logger.addHandler(__handler)

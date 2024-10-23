import logging
import logging.config

# Define logging configuration
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "memory": {
            "class": "logging.handlers.MemoryHandler",
            "capacity": 1000,
            "flushLevel": logging.ERROR,  # Flush when an ERROR log is encountered
            "target": "file"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "simple"
        }
    },
    "loggers": {
        "my_logger": {
            "level": "DEBUG",  # Capture all levels from DEBUG and above
            "handlers": ["memory"],
            "propagate": False
        }
    }
}

# Configure logging
logging.config.dictConfig(logging_config)

# Create a logger
logger = logging.getLogger('my_logger')

# Before logging messages
print("Logging configuration loaded. Starting to log messages...")

# Log some messages
logger.debug('This is a debug message')

for i in range(500):
    logger.info(f'This is an info message {i+1}')  # Log info messages with a counter

# After logging messages
print("Finished logging messages.")



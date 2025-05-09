import logging.config

# Not required to load the logger config here, gunicorn do it
logging.config.fileConfig("config/logging.ini")

logging.captureWarnings(True)
logging.getLogger("py.warnings").setLevel(logging.ERROR)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

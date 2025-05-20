import logging.config

logging.config.fileConfig("config/logging.ini")

logging.captureWarnings(True)
logging.getLogger("google.auth").setLevel(logging.WARNING)
logging.getLogger("py.warnings").setLevel(logging.ERROR)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.WARNING)
logging.getLogger("torio._extension.utils").setLevel(logging.WARNING)

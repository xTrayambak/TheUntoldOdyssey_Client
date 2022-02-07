import logging
import sys

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

def log(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.INFO)
    logger.log(logging.INFO, msg = f"[{sender}/INFO]: {msg}")

def warn(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.WARN)
    logger.log(logging.WARN, msg = f"[{sender}/WARN]: {msg}")

def fatal(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.FATAL)
    logger.log(logging.FATAL, msg = f"[{sender}/FATAL]: {msg}")
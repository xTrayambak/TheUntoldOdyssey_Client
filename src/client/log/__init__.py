import logging
import sys

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

def log(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.INFO)
    logger.log(logging.INFO, msg = f"[{sender}]: {msg}")
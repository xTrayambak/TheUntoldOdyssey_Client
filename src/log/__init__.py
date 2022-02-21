import logging
import sys

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))

class Color:
    '''
    ANSI escape codes for colored terminal.
    '''
    RESET = "\u001b[0m"
    RED = "\u001b[31m"

def log(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.INFO)
    logger.log(logging.INFO, msg = f"[{sender}/INFO]: {msg}")

def warn(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.WARN)
    logger.log(logging.WARN, msg = f"[{sender}/WARN]: {msg}")

def fatal(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.FATAL)
    logger.log(logging.FATAL, msg = f"{Color.RED}[{sender}/FATAL]: {msg}{Color.RESET}")
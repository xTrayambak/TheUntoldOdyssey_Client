import logging
import sys
from datetime import datetime

time_now = datetime.now()

date_info = time_now.strftime("%d-%m-%y")
time_info = time_now.strftime('%H %M %S')

fileHandler = logging.FileHandler(
    f'assets/logs/{date_info} {time_info}'
)
logger = logging.getLogger()
logger.addHandler(fileHandler)
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
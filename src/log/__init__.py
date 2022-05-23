import logging
import sys
from colorama import Fore
import traceback
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

def log(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.INFO)
    logger.log(logging.INFO, msg = f"{Fore.GREEN}[{sender}/INFO]: {msg}{Fore.RESET}")

def warn(msg = "Hello, World!", sender = "Worker/Thread-1", err = None):
    logger.setLevel(logging.WARN)
    if err and isinstance(err, Exception):
        logger.log(logging.WARN, msg = f"{Fore.RED}[{sender}/WARN]: {msg}")
        traceback.print_exception(err)
        logger.log(logging.WARN, msg = f"{Fore.RESET}")
    else:
        logger.log(logging.WARN, msg = f"{Fore.RED}[{sender}/WARN]: {msg}{Fore.RESET}")

def fatal(msg = "Hello, World!", sender = "Worker/Thread-1"):
    logger.setLevel(logging.FATAL)
    logger.log(logging.FATAL, msg = f"{Fore.LIGHTRED_EX}[{sender}/FATAL]: {msg}{Fore.RESET}")
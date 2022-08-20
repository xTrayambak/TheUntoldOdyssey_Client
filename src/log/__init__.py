import logging
import sys
import os
import threading

try:
    from colorama import Fore
except:
    Fore = None

import traceback
from datetime import datetime

time_now = datetime.now()

date_info = time_now.strftime("%d-%m-%y")
time_info = time_now.strftime('%H %M %S')

try:
    fileHandler = logging.FileHandler(
        f'assets/logs/{date_info} {time_info}'
    )
except FileNotFoundError:
    fileHandler = None

if os.path.exists('DEBUG_MODE'):
    fileHandler = None

# Scopes are evil. I say they are EVIIIIILLLLLL!!!
conf = {'enabled': True}

logger = logging.getLogger()
if fileHandler: logger.addHandler(fileHandler)
logger.addHandler(logging.StreamHandler(sys.stdout))

def set_enabled(value: int):
    if value == 0:
        conf['enabled'] = True
    else:
        #sys.stdout = None
        conf['enabled'] = False

def log(msg = "Hello, World!", sender = f"Worker/Thread-{threading.get_ident()}"):
    if not conf['enabled']: return
    logger.setLevel(logging.INFO)
    if Fore:
        logger.log(logging.INFO, msg = f"{Fore.GREEN}[{sender}/INFO]: {msg}{Fore.RESET}")
    else:
        logger.log(logging.INFO, msg = f"[{sender}/INFO]: {msg}")

def warn(msg = "Hello, World!", sender = f"Worker/Thread-{threading.get_ident()}", err = None):
    if not conf['enabled']: return
    logger.setLevel(logging.WARN)
    if err and isinstance(err, Exception):
        if Fore:
            logger.log(logging.WARN, msg = f"{Fore.RED}[{sender}/WARN]: {msg}")
        else:
            logger.log(logging.INFO, msg = f"[{sender}/WARN]: {msg}")
        traceback.print_exception(err)
        if Fore:
            logger.log(logging.WARN, msg = f"{Fore.RESET}")
    else:
        if Fore:
            logger.log(logging.WARN, msg = f"{Fore.RED}[{sender}/WARN]: {msg}{Fore.RESET}")
        else:
            logger.log(logging.INFO, msg = f"[{sender}/WARN]: {msg}")

def fatal(msg = "Hello, World!", sender = f"Worker/Thread-{threading.get_ident()}"):
    if not conf['enabled']: return
    logger.setLevel(logging.FATAL)
    if Fore:
        logger.log(logging.FATAL, msg = f"{Fore.LIGHTRED_EX}[{sender}/FATAL]: {msg}{Fore.RESET}")
    else:
        logger.log(logging.FATAL, msg = f"[{sender}/FATAL]: {msg}")

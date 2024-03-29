# lib/logger.py - Logging class and functions.
__version__ = '0.2'
__all__ = ['Log', 'LOG_LEVEL', 'LOG_DIR', 'LOGFILE_NAME']
#import inspect
import os
import logging
import traceback

from common.utils import ddict


# Sensible defaults
LOG_LEVEL = 'DEBUG'
LOG_DIR = 'logs/' or mkdir('logs')
LOGFILE_NAME = 'debug.log'
FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


os.system("touch logs/debug.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(LOG_DIR + LOGFILE_NAME)
handler.setLevel(logging.DEBUG)

formatter = FORMAT
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.info('Logger initialised by '+' '.join(traceback.format_stack()[0].split()[1:4]))


class Log(object):

    def __init__(self):
        logger.info('Log class initalised by '+' '.join(traceback.format_stack()[0].split()[1:4]))

    @staticmethod
    def info(msg):
        logger.info(msg)

    @staticmethod
    def warn(msg):
        logger.warn(msg)

    @staticmethod
    def debug(msg):
        logger.debug(msg)


def is_debug():
    return logging.getLogger("logger").getEffectiveLevel() == logging.DEBUG


def log(logmsg, lvl='INFO', e=None):
    if e:
        err = ' ('+str(e)+')'+' ERROR: ' + repr(e)
    else:
        err = ''
    logging.lvl(' ' + logmsg + err)


# @TODO: move into common/colors.py ?
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# print(f"{bcolors.OKGREEN}Lumberjack Logging Enabled{bcolors.RESET}")


"""
# Flask config loader.
except Exception as e:
    log("Error finding or loading DevelopmentConfig object. You probably need to specify package since Python 3 dropped support for relative import. (See PEP 8)", e)
    try:
        app.config.from_pyfile('config.py')
        log("Loaded configuration from file")
    except IOError:
        log("Error finding config.py", IOError)
    except EOFError:
        log("Error reading config.py (lint file)", EOFError)
    except Exception as e:
        log("Ignoring unknown exception when loading config.py", e)
    except:
        handle_unhandled_error()
        log("no idea.")
"""

import logging
import shutil
import time
import textwrap
from logging.handlers import RotatingFileHandler
from mongodb_management import env
from enum import Enum

console_logger = logging.getLogger("console_logger")
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(env["console_format"]))
console_logger.addHandler(console_handler)
console_logger.setLevel(logging.INFO)

file_logger = logging.getLogger("file_logger")
file_handler = RotatingFileHandler('bot_logs.txt', maxBytes=5*1024*1024, backupCount=2)
file_handler.setFormatter(logging.Formatter(env["file_format"], env["date_format"]))
file_logger.addHandler(file_handler)
file_logger.setLevel(logging.INFO)

def format_log(message, color_code):
    console_width = shutil.get_terminal_size().columns
    timestamp = time.strftime(env["date_format"])

    lines = textwrap.wrap(message, width=console_width - len(timestamp) - 1)
    lines[-1] += ' ' * (console_width - len(lines[-1]) - len(timestamp)) + timestamp
    lines = [line.ljust(console_width) for line in lines]

    formatted_message = '\n'.join(lines)

    if color_code:
        formatted_message = f"\033[48;5;{color_code}m{formatted_message}\033[0m"

    formatted_message = f"\033[48;5;{color_code}m{formatted_message}\033[0m" if color_code else formatted_message

    return formatted_message

class LogLevel(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    DEBUG = 4

def log(message, type=None):
    types = {
        LogLevel.INFO: ('INFO', env["INFO_color"]),
        LogLevel.WARNING: ('WARNING', env["WARNING_color"]),
        LogLevel.ERROR: ('ERROR', env["ERROR_color"]),
        LogLevel.DEBUG: ('DEBUG', env["DEBUG_color"])
    }

    if not env["debug_mode"] and type == LogLevel.DEBUG:
        return
    
    message_text, color_code = types.get(type, (None, None))
    message = f'{message_text}: {message}' if message_text else message
    
    formatted_message = format_log(message, color_code)

    console_logger.info(formatted_message)
    file_logger.info(message)

# Hyperlink support for console awaiting implementation

def hyperlink(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)
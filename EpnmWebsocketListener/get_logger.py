import sys
import logging
import pathlib
from typing import List, Literal


DEFAULT_LOG_PATH = pathlib.Path(__file__).resolve().parent.joinpath('epnm_websocket.log')
VERBOSITY_MAP = {
    1: logging.CRITICAL,
    2: logging.ERROR,
    3: logging.WARNING,
    4: logging.INFO,
    5: logging.DEBUG
}

def get_logger(name: str, verbosity=4, handle: List[Literal['stderr', 'stdout', 'file']] = ['stderr', 'file'], logfile_path: pathlib.Path = None) -> logging.Logger:

    if logfile_path is not None:
        if not isinstance(logfile_path, pathlib.Path):
            try:
                logfile_path = pathlib.Path(logfile_path).resolve()
            except Exception as e:
                print("Failed to process path to logfile. Fallback to default.")
                logfile_path = DEFAULT_LOG_PATH
    else:
        logfile_path = DEFAULT_LOG_PATH

    handlers = {
        'stderr': {
            'handler': logging.StreamHandler(sys.stderr),
            'required': 'stderr' in handle,
            'present': False
        },
        'stdout': {
            'handler': logging.StreamHandler(sys.stdout),
            'required': 'stdout' in handle,
            'present': False
        },
        'file': {
            'handler': logging.FileHandler(logfile_path, delay=True),
            'required': 'file' in handle,
            'present': False
        },
    }
    formatter_string = '[%(asctime)s] [%(levelname)s]\t[%(name)s][%(module)s][%(funcName)s]\t%(message)s'
    formatter = logging.Formatter(formatter_string)
    [x['handler'].setFormatter(formatter) for x in handlers.values()]

    logger = logging.getLogger(name=name)
    logger.propagate = 0
    logger.setLevel(VERBOSITY_MAP[verbosity])
    current_handlers = logger.handlers

    for handler in current_handlers:
        if isinstance(handler, logging.StreamHandler):
            if handler.stream == sys.stderr:
                handlers['stderr']['present'] = True
            if handler.stream == sys.stdout:
                handlers['stdout']['present'] = True
        if isinstance(handler, logging.FileHandler):
            handlers['file']['present'] = True

    for name, status in handlers.items():
        if status['required'] and status['present']:
            # print(f"Handler {name} already present")
            pass
        elif status['required'] and not status['present']:
            # print(f"Adding handler {name}")
            logger.addHandler(status['handler'])


    return logger

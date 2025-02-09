'''
support functions
'''

'''
packages
'''

from pathlib import Path
import os

'''
logger
'''

import logging
logger = logging.getLogger(__name__)

'''
functions
'''

def set_up_logger(log_path:str, log_file:str, root_logger:logging.Logger, log_level:int = logging.INFO) -> None:
    '''
    Logger Set-Up Function

    This function sets the properties of a logger.  This fucntion creates a file and
    stream and stream handler, ensures the directory is created for the log file, if not
    given sets the default log level to INFO and formats the log string.

    :param str log_path: path for the log file; can be absolute for relative
    :param str log_file: the file name for the log file
    :param logging.Logger root_logger: logger to configure
    :param int log_level: logging level; can be an of logging.DEBUG, logging.INFO,  
        logging.WARNING, logging.ERROR, logging.CRITICAL

    .. note:: this function should be called at the beginning of a script

    Example::

        logger = logging.getLogger('root')
        set_up_logger('./logs', 'controller.log', logger)
    '''
    # check file path for log file
    log_path = Path(log_path)
    log_file = log_file
    if not log_path.exists():
        log_path.mkdir(parents = True, exist_ok = True)

    # create path & file
    string_log_pf = os.path.join(str(log_path), log_file)

    # set-up logger
    root_logger.setLevel(log_level)

    # logging file handler & stream handler
    file_handler = logging.FileHandler(string_log_pf)
    stream_handler = logging.StreamHandler()

    # logging lowest level
    file_handler.setLevel(log_level)
    stream_handler.setLevel(log_level)

    # logging formatter
    string_msg_formatter = '%(asctime)s || %(filename)s || %(funcName)s || line: %(lineno)d || %(levelname)s || %(message)s'
    string_date_formatter = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(string_msg_formatter, string_date_formatter)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # add logging handler
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
    
    return None

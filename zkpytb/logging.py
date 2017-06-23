import logging
import logging.config
from pathlib import Path


mylogger = logging.getLogger('zkpytb.logging')


def setup_simple_console_and_file_logger(logger_name, logfile=True,
                                         logdir=None, logfilename=None,
                                         log_level='DEBUG', options=None):
    """
    TODOC
    """

    if options is None:
        options = {}

    # default values
    do_file_logging = True
    log_directory = Path('.')
    log_filename = logger_name + '.log'

    if logdir is not None:
        try:
            log_directory = Path(logdir)
        except TypeError as e:
            mylogger.exception('Invalid type for argument "logdir". '
                               'Expected "str", "bytes" or "pathlib.Path". '
                               'Received type: {}'.format(type(logdir)))
            do_file_logging = False
        else:
            if not logdir.is_dir():
                mylogger.warning('The given logdir is not a directory!')
                do_file_logging = False

    if not logfile:
        do_file_logging = False

    if logfilename is not None:
        log_filename = logfilename

    log_filepath = log_directory / log_filename

    default_format_str = '{asctime},{msecs:0>3.0f} - {levelname:8} - {message}'
    format_str = options.get('format_str', default_format_str)

    default_datefmt_str = '%Y-%m-%d %H:%M:%S'
    datefmt_str = options.get('datefmt_str', default_datefmt_str)

    console_formatter = options.get('console_formatter', 'normal_extra_newlines')
    file_formatter = options.get('file_formatter', 'normal')

    console_handler = {
        'level': log_level,
        'class': 'logging.StreamHandler',
        'formatter': console_formatter
    }

    file_handler = {
        'level': log_level,
        'class': 'logging.FileHandler',
        'formatter': file_formatter,
        'filename': log_filepath,
    }

    logging_conf = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'normal': {
                'format': format_str,
                'datefmt': datefmt_str,
                'style': '{'
            },
            'normal_extra_newlines': {
                'format': format_str + '\n',
                'datefmt': datefmt_str,
                'style': '{'
            },
        },
        'handlers': {
            'console': console_handler
        },
        'loggers': {
            logger_name: {
                'handlers': ['console'],
                'level': log_level,
            },
        }
    }

    if do_file_logging:
        logging_conf['handlers']['file'] = file_handler
        logging_conf['loggers'][logger_name]['handlers'].append('file')

    logging.config.dictConfig(logging_conf)
    logger = logging.getLogger(logger_name)

    return logger

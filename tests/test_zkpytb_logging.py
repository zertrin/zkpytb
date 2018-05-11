#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `logging` module of `zkpytb` package."""

import logging
import pytest
from pathlib import Path
# from testfixtures import Comparison as C, compare
from testfixtures import LogCapture

from zkpytb.logging import setup_simple_console_and_file_logger


loglevels = 'CRITICAL,ERROR,WARNING,INFO,DEBUG'.split(',')

loglevel_ranks = {
    'CRITICAL': 1,
    'ERROR': 2,
    'WARNING': 3,
    'INFO': 4,
    'DEBUG': 5,
}


@pytest.fixture(scope='module',
                params=loglevels)
def a_log_level(request):
    return request.param


def log_some_messages(logger, level='DEBUG'):
    max_rank = loglevel_ranks[level]
    if max_rank >= 1:
        logger.critical('critical message')
    if max_rank >= 2:
        logger.error('error message')
    if max_rank >= 3:
        logger.warning('warning message')
    if max_rank >= 4:
        logger.info('info message')
    if max_rank >= 5:
        logger.debug('debug message')


def expected_some_messages(logger_name, level='DEBUG'):
    expected_messages = []
    max_rank = loglevel_ranks[level]
    if max_rank >= 1:
        expected_messages.append((logger_name, 'CRITICAL', 'critical message'))
    if max_rank >= 2:
        expected_messages.append((logger_name, 'ERROR', 'error message'))
    if max_rank >= 3:
        expected_messages.append((logger_name, 'WARNING', 'warning message'))
    if max_rank >= 4:
        expected_messages.append((logger_name, 'INFO', 'info message'))
    if max_rank >= 5:
        expected_messages.append((logger_name, 'DEBUG', 'debug message'))
    return expected_messages


def test_setup_simple_console_and_file_logger_1():
    """
    Test the case without file logging.
    """
    logger_name = 'logtest1'
    with LogCapture('zkpytb.logging') as lc2:
        logger = setup_simple_console_and_file_logger(logger_name, logfile=False)
    assert len(lc2.records) == 0
    assert len(logger.handlers) == 1
    assert logger.level == logging.DEBUG
    with LogCapture(logger_name) as lc1:
        log_some_messages(logger)
    lc1.check(*expected_some_messages(logger_name))
    log_filename = logger_name + '.log'
    log_filepath = Path('.') / log_filename
    assert not log_filepath.exists()


def test_setup_simple_console_and_file_logger_2(tmpdir):
    """
    Test the case with file logging.
    """
    logger_name = 'logtest2'
    with LogCapture('zkpytb.logging') as lc2:
        logger = setup_simple_console_and_file_logger(logger_name, logdir=str(tmpdir))
    assert len(lc2.records) == 0
    assert len(logger.handlers) == 2
    log_some_messages(logger)
    log_filename = logger_name + '.log'
    log_filepath = Path(str(tmpdir)) / log_filename
    assert log_filepath.is_file()
    with open(str(log_filepath), 'r') as f:
        lines = f.readlines()
    assert len(lines) == 5
    for i, logtuple in enumerate(expected_some_messages(logger_name)):
        assert logtuple[1] in lines[i]
        assert logtuple[2] in lines[i]


def test_setup_simple_console_and_file_logger_3(tmpdir):
    """
    Test the case where the log directory does not exists.
    """
    logger_name = 'logtest3'
    with LogCapture('zkpytb.logging') as lc2:
        logger = setup_simple_console_and_file_logger(logger_name, logdir=str(tmpdir) + '_nonexistent')
    lc2.check(('zkpytb.logging', 'WARNING', 'The given logdir is not a directory!'))
    assert len(logger.handlers) == 1
    with LogCapture(logger_name) as lc1:
        log_some_messages(logger)
    lc1.check(*expected_some_messages(logger_name))
    log_filename = logger_name + '.log'
    log_filepath = Path(str(tmpdir)) / log_filename
    assert not log_filepath.exists()


def test_setup_simple_console_and_file_logger_4(tmpdir):
    """
    Test the case where the logdir is of invalid type.
    """
    logger_name = 'logtest4'
    with LogCapture('zkpytb.logging') as lc2:
        logger = setup_simple_console_and_file_logger(logger_name, logdir=123)
    err_msg = ('Invalid type for argument "logdir". '
               'Expected "str", "bytes" or "pathlib.Path". '
               'Received type: {}'.format(type(123)))
    lc2.check(('zkpytb.logging', 'ERROR', err_msg))
    assert len(logger.handlers) == 1
    with LogCapture(logger_name) as lc1:
        log_some_messages(logger)
    lc1.check(*expected_some_messages(logger_name))
    log_filename = logger_name + '.log'
    log_filepath = Path('.') / log_filename
    assert not log_filepath.exists()


def test_setup_simple_console_and_file_logger_5(tmpdir):
    """
    Test the case where the logfile name is supplied by the user.
    """
    logfilename = 'loremipsum.log'
    logger_name = 'logtest5'
    with LogCapture('zkpytb.logging') as lc2:
        logger = setup_simple_console_and_file_logger(logger_name, logdir=str(tmpdir),
                                                      logfilename=logfilename)
    assert len(lc2.records) == 0
    assert len(logger.handlers) == 2
    log_some_messages(logger)
    log_filepath = Path(str(tmpdir)) / logfilename
    assert log_filepath.is_file()
    with open(str(log_filepath), 'r') as f:
        lines = f.readlines()
    assert len(lines) == 5
    for i, logtuple in enumerate(expected_some_messages(logger_name)):
        assert logtuple[1] in lines[i]
        assert logtuple[2] in lines[i]


def test_setup_simple_console_and_file_logger_6(tmpdir):
    """
    Test the case with extra options and at the same time the case with different file formatting.
    """
    logger_name = 'logtest6'
    options = {'file_formatter': 'normal_extra_newlines'}
    with LogCapture('zkpytb.logging') as lc2:
        logger = setup_simple_console_and_file_logger(logger_name, logdir=str(tmpdir), options=options)
    assert len(lc2.records) == 0
    assert len(logger.handlers) == 2
    log_some_messages(logger)
    log_filename = logger_name + '.log'
    log_filepath = Path(str(tmpdir)) / log_filename
    assert log_filepath.is_file()
    with open(str(log_filepath), 'r') as f:
        lines = f.readlines()
    assert len(lines) == 10
    for i, logtuple in enumerate(expected_some_messages(logger_name)):
        assert logtuple[1] in lines[2 * i]
        assert logtuple[2] in lines[2 * i]


def test_setup_simple_console_and_file_logger_7(a_log_level):
    """
    Test the case without file logging and with different log levels.
    """
    logger_name = 'logtest7'
    with LogCapture('zkpytb.logging') as lc2:
        logger = setup_simple_console_and_file_logger(logger_name, logfile=False, log_level=a_log_level)
    assert len(lc2.records) == 0
    assert len(logger.handlers) == 1
    assert logger.level == getattr(logging, a_log_level)
    with LogCapture(logger_name) as lc1:
        log_some_messages(logger, level=a_log_level)
    lc1.check(*expected_some_messages(logger_name, level=a_log_level))
    log_filename = logger_name + '.log'
    log_filepath = Path('.') / log_filename
    assert not log_filepath.exists()

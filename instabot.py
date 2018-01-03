#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""instabot ...an instagram bot.

Usage:
  instabot.py [CNF] [options]

Arguments:
  CNF                        config file [default: config.yml]

Options:
  --log=<level>              log level [default: DEBUG]
  --version                  show program's version number and exit
  -h, --help                 show this help message and exit

"""

import logging
import os
import sys
from pathlib import Path

import yaml
from docopt import docopt
from instapy import InstaPy

logger = logging.getLogger('instabot')

VERSION = '0.1'
CONFIG = './config.yml'


def cd_insta_path():
    global bot_path
    bot_path = str(Path(__file__).resolve().parent)

    try:
        instapy_path = '{0}/src/instapy'.format(os.environ['VIRTUAL_ENV'])
    except KeyError as error:
        logger.critical('VIRTUAL_ENV var not set: %s', error)
        sys.exit(5)

    logger.debug('instapy path: %s', instapy_path)

    if bot_path == instapy_path:
        logger.critical('bot must not be installed over instapy dir')
        sys.exit(5)

    try:
        os.chdir(instapy_path)
    except FileNotFoundError:
        logger.critical('cant access %s path', instapy_path)
        sys.exit(5)

    logger.info('positioned in instapy')

    return None


def get_config(config_file):
    with open(config_file) as stream:
        return yaml.load(stream)


def set_logger(log_level):
    level = logging.getLevelName(log_level.upper())
    fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    logger.setLevel(level)
    handler.setLevel(level)
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    return None


def get_session():

    session = InstaPy(
        username=os.environ['INSTAUSER'],
        password=os.environ['INSTAPASS']
    )
    session.login()

    return session


def main(arguments):
    config = arguments['CNF'] if arguments['CNF'] is not None else CONFIG
    log_level = arguments['--log']

    set_logger(log_level)

    try:
        config_file = get_config(config)
    except FileNotFoundError:
        logger.critical('unable to read file: %s', config)
        return None

    cd_insta_path()

    try:
        session = get_session()
    except KeyError as error:
        logger.critical('env var not set: %s', error)
        return None
    except Exception as error:
        logger.critical('unable to login: %s', error)
        return None

    session.end()

    try:
        os.chdir(bot_path)
    except:
        pass
    else:
        logger.info('positioned in bot dir')

    return None


if __name__ == '__main__':
    main(docopt(__doc__, version=VERSION))

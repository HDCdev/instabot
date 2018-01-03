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

import yaml
from instapy import InstaPy

from docopt import docopt

logger = logging.getLogger('instabot')

VERSION = '0.1'
CONFIG = './config.yml'


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

    try:
        session = get_session()
    except KeyError as error:
        logger.critical('env var not set: %s', error)
        return None
    except Exception as error:
        logger.critical('unable to login: %s', error)
        return None

    session.end()

if __name__ == '__main__':
    main(docopt(__doc__, version=VERSION))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""instabot ...an instagram bot.

Usage:
  instabot.py [CNF] [options]

Arguments:
  CNF                        config file [default: config.yml]

Options:
  --follow=<username>        follow someone else's followers/following
  --like=<option>            like posts by [tags|feed]
  --tags=<tags>              tags to track
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


def follower(target):

    follow_set = config_file['follow']['set']
    logger.debug('follow sets: %s', str(follow_set))
    session.set_do_follow(**follow_set)

    follow_kwargs = config_file['follow']['kwargs']
    logger.debug('follow kwargs: %s', str(follow_kwargs))
    session.follow_user_followers(target, **follow_kwargs)

    return None


def liker(mode, params_tags=None):

    like_set = config_file['like']['set']
    logger.debug('like sets: %s', str(like_set))
    session.set_do_like(**like_set)

    like_kwargs = config_file['like']['kwargs']
    logger.debug('like kwargs: %s', str(like_kwargs))

    if mode == 'tags':
        tags = config_file['like']['tags']

        if params_tags:
            tags += params_tags

        session.like_by_tags(tags, **like_kwargs)
    else:
        session.like_by_feed(**like_kwargs)

    return None


def main(arguments):
    config = arguments['CNF'] if arguments['CNF'] is not None else CONFIG
    follow = arguments['--follow']
    like = arguments['--like']
    tags = arguments['--tags']
    log_level = arguments['--log']

    set_logger(log_level)

    global config_file

    try:
        config_file = get_config(config)
    except FileNotFoundError:
        logger.critical('unable to read file: %s', config)
        return None

    cd_insta_path()

    global session

    try:
        session = get_session()
    except KeyError as error:
        logger.critical('env var not set: %s', error)
        return None
    except Exception as error:
        logger.critical('unable to login: %s', error)
        return None

    if follow is not None:
        target = follow.split(',')
        follower(target)

    if like is not None:
        like = like.lower()
        if like  in ['tags', 'feed']:
            if tags is not None:
                tags = tags.split(',')
            liker(like, params_tags=tags)
        else:
            logger.critical('%s not a valid like option', like)

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

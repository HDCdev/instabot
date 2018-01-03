#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from instapy import InstaPy


logger = logging.getLogger('instabot')


def get_session():

    session = InstaPy(
        username=os.environ['INSTAUSER'],
        password=os.environ['INSTAPASS']
    )
    session.login()

    return session

def main():
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
    main()


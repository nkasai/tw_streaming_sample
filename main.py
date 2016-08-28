#!/bin/env python3
# -*- coding: UTF-8 -*-
'''
Created on 2016/08/28

@author: nkasai
'''
import logging
import argparse
import tweepy

#
# settings
#
CONSUMER_KEY = ' enter your cunsumer key.'
CONSUMER_SECRET = 'enter your consumer secret.'
ACCESS_TOKEN = 'enter your access token.'
ACCESS_TOKEN_SECRET = 'enter your access token secret'

ASYNC = False
TRACK = [
    'george harrison',
]
LANGUAGES = [
    'ja',
]

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = '/var/log/tw_streaming_sample.log'
LOG_FORMAT = '%(asctime)s line:%(lineno)d [%(levelname)s] %(message)s'

#
# logging
#
logger_ = logging.getLogger()
logger_.setLevel(LOG_LEVEL)
logHandler = logging.FileHandler(filename=LOG_FILENAME)
logHandler.setFormatter(logging.Formatter(LOG_FORMAT))
logger_.addHandler(logHandler)

class MyStreamListener(tweepy.StreamListener):
    """
    MyStreamListener
    """

    def __init__(self, api=None):
        """
        init
        """
        super(MyStreamListener, self).__init__(api)

    def on_connect(self):
        """
        on_connect
        """
        logging.info('connectted.')

    def on_status(self, status):
        """
        on_status
        """
        id_ = status.id
        text = status.text
        screen_name = status.user.screen_name
        user_name = status.user.name
        in_reply_to_user_id = status.in_reply_to_user_id
        retweeted = status.retweeted

        logging.debug('id : %s', id_)
        logging.debug('screen_name : %s', screen_name)
        logging.debug('user_name : %s', user_name)
        logging.debug('text : %s', text)
        logging.debug('in_reply_to_user_id : %s', in_reply_to_user_id)
        logging.debug('retweeted : %s', retweeted)
        
        # retweet
        #status.retweet(id_)

    def on_limit(self, track):
        """
        on_limit
        """
        logging.warning('limitation notice arrives : %s', track)

    def on_error(self, status_code):
        """
        on_error
        """
        logging.error('error notice arrives : %s', status_code)

        if status_code == 420:
            return False

    def on_timeout(self):
        """
        on_timeout
        """
        logging.error('timeout.')

    def on_disconnect(self, notice):
        """
        on_disconnect
        """
        logging.info('disconnectted.')

    def on_warning(self, notice):
        """
        on_warning
        """
        logging.warning('a disconnection warning message arrives : %s', notice)

def main(args):
    """
    main
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    listener = MyStreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=listener)

    stream.filter(
        track=TRACK,
        async=ASYNC,
        languages=LANGUAGES
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='streaming api sample.')
    #parser.add_argument('--target', required=True)
    args = parser.parse_args()

    main(args)


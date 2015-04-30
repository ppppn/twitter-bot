#!/usr/bin/python
# coding: UTF-8
from tweepy.error import TweepError
import random
import re
from const import *
from tweets import tweets
import logging
from API import GetAPI

logging.basicConfig(level=LOGLEVEL)

api = None

def PostRegularTweet():
  __name__ = "PostRegularTweet()"
  global api
  num_max_tw = len(tweets) -1 
  error_counter = 0
  while error_counter < ERROR_LIMIT:
    try:
      random.seed()
      tw_num = random.randint(0, num_max_tw)
      selected_tweet = tweets[tw_num]
      api.update_status(selected_tweet)
      logging.debug("%s: Tweeted> '%s'", __name__, selected_tweet )
      logging.info("%s: Regular tweet successfully posted.", __name__)
      return True
    except TweepError, e:
      logging.error("%s: %s", __name__, e.reason)
      error_counter += 1
  logging.error("%s: Failed to post a regular tweet %d times. Aborted.", __name__, ERROR_LIMIT)

def FollowBack():
  __name__ = "FollowBack()"
  global api
  error_counter = 0
  followback_counter = 0
  while error_counter < ERROR_LIMIT:
    try:
      FollowerList = api.followers()
      for follower in FollowerList:
        if follower.following == False and follower.follow_request_sent == False:
          api.create_friendship(follower.screen_name)
          logging.debug("Follow back:" + follower.screen_name)
          followback_counter += 1
      logging.info("%s: Followed back %d account(s)", __name__, followback_counter)
      return True
    except TweepError, e:
      logging.error("%s: %s", __name__, e.reason)
  logging.error("%s: Failed to follow back %d times. Aborted.", __name__, ERROR_LIMIT)

def main():
  global api
  api = GetAPI()
  PostRegularTweet()
  FollowBack()


if __name__ == "__main__":
  main()

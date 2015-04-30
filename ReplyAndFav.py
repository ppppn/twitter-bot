#!/usr/bin/python
# coding: UTF-8
from tweepy.error import TweepError
import random
import re
from const import *
from words import *
from replies import replies
import datetime
import logging
from API import GetAPI

logging.basicConfig(level=LOGLEVEL)

api = None

# 説明

# 関数リスト 

# FUNCTION_NAME(args) > Returns(SUCCESS, FAILED)

# FetchHomeTL() > (TIMELINE, False)
# FormattingAndTweetForReply(status, content) > (True, False)
# CheckAndReplyToSpecialWord(account_screen_name, status) > (True, False)
# CheckAndReplyToNormalTweet(status) > (True, False)
# CheckAndCreateFav(status) > (True, False)

def UpdateAndNotifyAccountInfo():
  __name__ = "UpdateAndNotifyAccountInfo()"
  global api
  account = api.me()
  try:
    if not account.name == BOT_NAME:
      api.update_status(UPDATE_MSG)
      api.update_profile(name=BOT_NAME)
      logging.info("%s: Successfully finished.", __name__)
  except TweepError, e:
    logging.error("%s: %s", __name__, e.reason)

def FetchHomeTL():
  __name__ = "FetchHomeTL()"
  global api
  since_id = api.user_timeline()[0].id
  logging.debug("%s: Last post id: %d", __name__, since_id)
  try:
    return api.home_timeline(since_id=since_id)
  except TweepError, e:
    logging.error("%s: %s", __name__, e.reason)
    return False



def FormattingAndTweetForReply(status, content): 
  __name__ = "FormattingAndTweetForReply()"
  global api
#ツイートを最終的に投稿される形にフォーマットし、投稿する
  error_counter = 0
  #{name}を相手の名前で置き換える
  content = content.format(name = status.author.name)
  #@hogehogeをつける
  formatted_tweet = "@" + status.author.screen_name + " " + content
  #投稿する
  while error_counter < ERROR_LIMIT:
    try:
      api.update_status(formatted_tweet, in_reply_to_status_id = int(status.id))
      logging.debug("%s: The following tweet was successfully posted> '%s'",
                                                  __name__, formatted_tweet)
      return True
    except TweepError, e:
      logging.error(e.reason)
      error_counter += 1
  
  logging.error("%s: Failed to post %d times. Aborted.", __name__, ERROR_LIMIT)
  return False

def CheckAndReplyToSpecialWord(account_screen_name, status):
  __name__ = "CheckAndReplyToSpecialWord()"
  global api
  error_counter = 0
  #ぼっと宛のメンションに限定
  if status.in_reply_to_screen_name == account_screen_name:
    for special_word in special_words:
      if re.search(special_word, status.text):
        logging.debug("%s: The special word '%s' was detected in %s's post '%s'", 
                      __name__, special_word, status.author.screen_name, status.text)
        num_max_patterns = len(special_words[special_word]) - 1
        while error_counter < ERROR_LIMIT:
          random.seed()
          selected_num = random.randint(0, num_max_patterns)
          content = special_words[special_word][selected_num]
          #重複投稿によるエラー防止のため時刻を追記
          content += " (%s)"%str(datetime.datetime.today())
          logging.debug("%s: Special word reply was generated> '%s'", __name__,  content)
          if FormattingAndTweetForReply(status, content):
            return True
          else:
            logging.error("%s: Reselect", __name__)
            error_counter += 1
        logging.error("%s: Failed to post %d times. Aborted.", __name__, ERROR_LIMIT)
        return False
    logging.debug("%s: No special word was founded in %s's post '%s'",
                  __name__, status.author.screen_name, status.text)
    return False
  else:
    return False

def CheckAndReplyToNormalTweet(status):
  __name__ = "CheckAndReplyToNormalTweet()"
  global api
  error_counter = 0
  num_max_tw = len(replies) - 1
  for word in reply_words:
    if re.search(word, status.text):
      logging.debug("%s: The reply word '%s' was detected in %s's post '%s'", 
                    __name__, word, status.author.screen_name, status.text)
      while error_counter < ERROR_LIMIT:
        random.seed()
        tw_num = random.randint(0, num_max_tw)
        content = replies[tw_num].format(name=status.author.name)
        logging.debug("%s: Normal word reply selected> '%s'", __name__, content)
        if FormattingAndTweetForReply(status, content):
          return True
        else:
          logging.error("%s: Reselect", __name__)
          error_counter += 1
        logging.error("%s: Failed to post %d times. Aborted.", __name__, ERROR_LIMIT)
  return False

def CheckAndCreateFav(status):
  __name__ = "CheckAndCreateFav()"
  global api
  if status.favorited == False:
    error_counter = 0
    for fav_word in fav_words:
      if re.search(fav_word, status.text):
        logging.debug("%s: Favorite word '%s' was detected in %s's post '%s'",
                      __name__, fav_word, status.author.screen_name,  status.text)
        while error_counter < ERROR_LIMIT:
          try:
            api.create_favorite(status.id)
            logging.debug("%s: Successfully favorited %s's post> '%s'", 
                        __name__, status.author.screen_name, status.text)
            return True
          except TweepError, e:
            logging.error(e.reason)
            error_counter += 1
        logging.error("%s: Failed to create fav %d times. Aborted.",
                                                    __name__, ERROR_LIMIT)
  return False

def main():
  global api
  api = GetAPI()
  UpdateAndNotifyAccountInfo()
  account_screen_name = api.me().screen_name
  tw_counter = 0
  fav_counter = 0
  result = False
  Timeline = FetchHomeTL()
  contains_excluded_word = False
  if Timeline == False:
    logging.critical("Failed to fetch home timeline. All processes are aborted.")
  else:
    for status in Timeline:
      contains_excluded_word = False
      if status.author.screen_name == account_screen_name:
        pass
        #ぼっとがツイートしたものは対象外
      else:
        #excluded_wordに登録された単語が含まれている場合、処理しない
        for excluded_word in excluded_words:
          if re.search(excluded_word, status.text):
            contains_excluded_word = True

        if contains_excluded_word == False:
          result = CheckAndReplyToSpecialWord(account_screen_name, status)
          if result == False:
            result = CheckAndReplyToNormalTweet(status)
          if result == True:
            tw_counter += 1
          result = CheckAndCreateFav(status)
          if result == True:
            fav_counter += 1

    logging.info("Reply: %d, Fav: %d", tw_counter, fav_counter)

if __name__ == "__main__":
  main()

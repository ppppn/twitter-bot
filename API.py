import tweepy
from const import *
def GetAPI():
	try:
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth)
		return api
	except tweepy.error.TweepError, e:
		logging.error(e.reason)

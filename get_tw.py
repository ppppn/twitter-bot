#!/usr/bin/python
# coding: UTF-8
import tweepy
import re
from const import *
import logging
from API import GetAPI


#APIセット
api = GetAPI()

#書き込み先ファイル
LAST_ID_FILENAME = "../data.shiroro_3_bot/last_id"
f_last_id = open(LAST_ID_FILENAME, "r")
last_id = int(f_last_id.readline())
usr_tl = api.user_timeline(ORIGINAL_ACCOUNT,count=800,since_id=int(last_id),)
usr_tl = sorted(set(usr_tl), key=usr_tl.index)

if len(usr_tl) > 0:
	newest_tw_id = usr_tl[0].id
	tweet_fname = "../data.shiroro_3_bot/" + str(newest_tw_id) + "tw"
	rep_fname = "../data.shiroro_3_bot/" +  str(newest_tw_id) + "rep"
	tweet_file = open(tweet_fname, "w")
	rep_file = open(rep_fname, "w")
	for tw in usr_tl:
		if re.search("RT @", tw.text):
			pass
		else:
			tw.text = re.sub("\n", "\\\\n", tw.text)
			if re.search("^@.* ", tw.text):
				tw.text = re.sub("^@.* ", "", tw.text)
				to_file = rep_file
			else:
				to_file = tweet_file
			line = "\tu\"" + tw.text + "\",\n"
			if re.search(u"(さん|ちゃん|君|くん|ねずみ|ネズミ|氏)", line):
				line = "#WARNING: The tweet/replies on the next line may includes someone's name!\n" + line
			to_file.write(line.encode("utf-8"))

	f_last_id = open(LAST_ID_FILENAME, "w")
	f_last_id.write(str(newest_tw_id))
	f_last_id.close()

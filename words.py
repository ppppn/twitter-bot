# coding: UTF-8
#除外ワード
excluded_words = [
	u'RT',
	u'dummy-exclude-word',
]

fav_words = [
	u' dummy-fav-words',
]

#TL上のツイート中に含まれていると返信するワード
reply_words = [
	'@this_account',
]

#指定されたリプを返すワード(メンションに対してのみ有効/主にゲームなどのちょっとした機能用)
#'反応ワード':['リプ1', 'リプ2', ...]のように記述
special_words = {
	u'dummy-special_word':[
		u'dummy-reply',
	],
}

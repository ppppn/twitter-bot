#! /usr/bin/python2.7
# Check whether moodules don't have errors by importing them
# Header


def SyntaxCheck():
  print " *Checking Syntax of each Modules..."

  module_names = ["tweets", "replies", "words", "const",]

  success = True

  for importing_module in module_names:
    print "  *%s.py\t\t\t\t\t\t" % importing_module,
    try:
      tmp = __import__(importing_module,globals(), locals() )
      #OK
      print "\x1b[33m\x1b[1mOK\x1b[0m\x1b[39m"
    except SyntaxError, e:
      #FAILED
      print "\x1b[31m\x1b[1mERROR\x1b[0m\x1b[39m"
      print "\t\t\tSyntax Error -> line:%d, offset:%d"%(e.lineno, e.offset)
      success = False

  return success

def CharacterLengthCheck():
  from tweets import tweets
  from replies import replies
  from words import special_words
  from const import UPDATE_MSG
  ERRORMSG_UPDATE_MSG = "The length of UPDATE_MSG in const.py seems to exceed 160 characters, the limit by Twitter"
  ERRORMSG_TWEET = "The length of the follwing tweet(s) seems to exceed 140 characters, the limit by Twitter"

  checking_list = [
     #(MODULE_NAME, MODULE, LIMIT, MSG)
      ("tweets", tweets, 140, ERRORMSG_TWEET),
      ("replies", replies, 140, ERRORMSG_TWEET),
    ]
  print " *Checking Length of Texts in each Modules..."
  for checking_module in checking_list:
    print "  *%s.py\t\t\t\t\t\t" % checking_module[0],
    warning_tweets = []
    for tweet_in_checking in checking_module[1]:
      if len(tweet_in_checking) > checking_module[2]:
        warning_tweets.append(tweet_in_checking)

    if len(warning_tweets) > 0:
      print ""
      print "     \x1b[31m\x1b[1mWARNING\x1b[0m\x1b[39m: ",
      print checking_module[3]
      for tweet_in_showing in warning_tweets:
        print "     ", tweet_in_showing
    else:
      print "\x1b[33m\x1b[1mOK\x1b[0m\x1b[39m"

  print "  *const.py\t\t\t\t\t\t",
  if len(UPDATE_MSG) > 140:
    print ""
    print "     \x1b[31m\x1b[1mWARNING\x1b[0m\x1b[39m: ",
    print ERRORMSG_UPDATE_MSG
  else:
    print "\x1b[33m\x1b[1mOK\x1b[0m\x1b[39m"

print "*Checking", __name__
success = SyntaxCheck()
if success == True:
  CharacterLengthCheck()

#!/usr/bin/python
#-------------------------------------------------------------------------------------
# Created by: Krishna Balam
# Date: 25-July-2015
# Purpose: news paper program that gives top 10 hot news from news and world news from reddit
# Change Log:
# Date               Name                  Description
#----------------------------------------------------------------------------
# 07/25/2015         Krishna Balam         Initial Creation
#

import praw
import argparse

def readNews(agentid, sub, ntype, num):
	redd = praw.Reddit(user_agent = agentid)
	
	if ntype.upper() == "HOT":
		getNews = redd.get_subreddit(sub).get_hot(limit=num)
	elif ntype.upper() == "NEW":
		getNews = redd.get_subreddit(sub).get_new(limit=num)
	elif ntype.upper() == "RISING":
		getNews = redd.get_subreddit(sub).get_rising(limit=num)
	elif ntype.upper() == "CONTROVERSIAL":
		getNews = redd.get_subreddit(sub).get_controversial(limit=num)
	elif ntype.upper() == "TOP":
		getNews = redd.get_subreddit(sub).get_top(limit=num)
	elif ntype.upper() == "GLIDED":
		getNews = redd.get_subreddit(sub).get_glided(limit=num)
	elif ntype.upper() == "PROMOTED":
		getNews = redd.get_subreddit(sub).get_promoted(limit=num)
	else:
		getNews = redd.get_subreddit(sub).get_hot(limit=num)
	
	return getNews

#---------------------------------------------------------------------
# Start Main Program here
#---------------------------------------------------------------------
# Asks user for for which sub reddit he wants to read from,and what type of news (hot, new so on )
# if nothing is supplied, it takes news as default subreddit and hot as type of posts for 10 ten

# Define parser to parse arguments
parser = argparse.ArgumentParser(description="This is a news paper program that reads from reddit")

# Add arguments
parser.add_argument('-s', action='store', dest='subReddit', default='news', 
					help='enter a subreddit that you are interested to read such as news, worldnews, julia, python, soccer. default is news')
parser.add_argument('-t', action='store', dest='newsType', default='hot',
					help='enter type of news you want to see, such as hot, new, rising, controversial, top, glided, promoted. default is hot')
parser.add_argument('-n', action='store', dest='howMany', default=10,
					help='enter how many to news you want to see, for e.g. 5, 10,15,20, 30 so on. default is 10')
parser.add_argument('-a', action='store', dest='appAgentID', 
					help='enter your app agent id for using API')
					
args = parser.parse_args()

# Welcome the user
print("Welcome to news paper program")
print("----------------------------------------------------------------")
print("")
print("You are reading from the subreddit: " + args.subReddit)
print("You are reading top %i %s news from subreddit %s" % (int(args.howMany), args.newsType, args.subReddit))
print("----------------------------------------------------------------")
	   
news = readNews(args.appAgentID, args.subReddit, args.newsType, int(args.howMany))

for x in news:
	   print(x)








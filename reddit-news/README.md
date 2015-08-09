''' python
./reddit_news.py --help
usage: reddit_news.py [-h] [-s SUBREDDIT] [-t NEWSTYPE] [-n HOWMANY]
                      [-a APPAGENTID]

This is a news paper program that reads from reddit

optional arguments:
  -h, --help     show this help message and exit
  -s SUBREDDIT   enter a subreddit that you are interested to read such as
                 news, worldnews, julia, python, soccer. default is news
  -t NEWSTYPE    enter type of news you want to see, such as hot, new, rising,
                 controversial, top, glided, promoted. default is hot
  -n HOWMANY     enter how many to news you want to see, for e.g. 5, 10,15,20,
                 30 so on. default is 10
  -a APPAGENTID  enter your app agent id for using API

import config
import tweepy
import csv
import schedule
import time
from datetime import datetime, timedelta

date_time_obj = datetime.strptime("20/06/16 04:00", '%y/%m/%d %H:%M')

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
key = config.access_key
secret = config.access_secret
timze_zone_diff_hour = int(config.time_zone_diff.split(':')[0])
timze_zone_diff_min = int(config.time_zone_diff.split(':')[1])

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

tweet_char_limit = 280
tweetId = ''


def tweet_tweet(texttotweetWithDatetime):
    #conver to UTC time
    utcDateTime = datetime.strptime(texttotweetWithDatetime[0], '%y/%m/%d %H:%M') 
    utcDateTime = utcDateTime + timedelta(hours=timze_zone_diff_hour,minutes=timze_zone_diff_min)

    time_diff_minutes = (datetime.now() - utcDateTime).total_seconds() / 60
    if (time_diff_minutes >= 1 and time_diff_minutes < 2):
        texttotweet = texttotweetWithDatetime[1]
        try:
            for i in range(0, len(texttotweet), tweet_char_limit):
                if(tweetId == ''):
                    tweetObj = api.update_status(texttotweet[i: i + tweet_char_limit])
                else:
                    tweetObj = api.update_status(texttotweet[i: i + tweet_char_limit], tweetObj.id)
        except tweepy.TweepError as e:
            print(e.reason)


def read_tweets():
    tweetsFile = open('tweetstopost.csv')
    tweetreader = csv.reader(tweetsFile)
    tweetlist = list(tweetreader)
    try:
        for line in tweetlist:
            if line != [] and datetime.strptime(line[0], '%y/%m/%d %H:%M').date() == datetime.today().date():
                tweet_tweet(line)
    except tweepy.TweepError as e:
        print(e.reason)

schedule.every(1).minutes.do(read_tweets)

while True:
    schedule.run_pending()
    time.sleep(1)



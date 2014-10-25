import sys
import csv
import argparse
import re
from pyechonest import song


__tagre = re.compile("@[a-zA-Z][a-zA-Z0-9]+")
def remove_tags(tweet):
    global __tagre
    return  __tagre.sub("", tweet)

__httpre = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
# Regex taken from Stackoverflow question:
# https://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python/6883094
def remove_url(tweet):
    global __httpre
    return __httpre.sub("", tweet)
    
__puncre = re.compile("[:;,.!?-]")
def remove_punctuation(tweet):
    global __puncre
    return __puncre.sub("", tweet)

__spacere1 = re.compile("^\s+")
__spacere2 = re.compile("\s\s+")
def remove_extra_space(tweet):
    global __spacere1
    global __spacere2
    result = __spacere1.sub("", tweet)
    result = __spacere2.sub(" ", result)
    return result

def clean_tweet(tweet):
    result = remove_url(tweet)
    result = remove_tags(result)
    result = remove_punctuation(result)
    result = remove_extra_space(result)
    return result

def get_song(tweet):
    text = tweet[5]
    print " *", text
    result = clean_tweet(text)
    print " -", result
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( "tweetfile",
                         help = "Source csv file for tweets." )
    parser.add_argument( "--num",
                         help = "Number of tweets to use.",
                         default = 5 )
    args = parser.parse_args()
    print "Using %s:" % args.tweetfile
    tweetfile = args.tweetfile
    numtweets = args.num
    with open(tweetfile) as fp:
        tweetcsv = csv.reader(fp)
        total = 0
        for tweet in tweetcsv:
            song = get_song(tweet)
            total = total + 1
            if total > numtweets:
                break

import sys
import csv
import argparse
import re
from pyechonest import song, config


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

__fillerre = re.compile(r"\b(?:the|a|an|and|is|am)\b", re.IGNORECASE)
def remove_filler_words(tweet):
    result = __fillerre.sub("", tweet)
    return result

def clean_tweet(tweet):
    result = remove_url(tweet)
    result = remove_tags(result)
    result = remove_punctuation(result)
    result = remove_extra_space(result)
    return result

def get_song(tweet):
    text = tweet[5]
    title = clean_tweet(text)
    try:
        results = song.search( title = title,
                               results = 1,
                               buckets = ['audio_summary'] )
        return results
    except:
        return []

if __name__ == "__main__":
    config.ECHO_NEST_API_KEY = "M2WEJZVEYOCWX8IAR"
    parser = argparse.ArgumentParser()
    parser.add_argument( "tweetfile",
                         help = "Source csv file for tweets." )
    parser.add_argument( "--num",
                         help = "Number of tweets to use.",
                         default = 5 )
    args = parser.parse_args()
    print "Using %s:" % args.tweetfile
    tweetfile = args.tweetfile
    numtweets = int(args.num)
    print "Numtweets:", numtweets
    with open(tweetfile) as fp:
        tweetcsv = csv.reader(fp)
        total = 0
        for tweet in tweetcsv:
            flag = False
            songs = get_song(tweet)
            for song in songs:
                print
                print "%d : %s" % (total, song)
                flag = True
            total = (total + 1) if flag else total
            print ".",
            # if numtweets != 0 and total >= numtweets:
            #     break
    print

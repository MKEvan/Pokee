#code to retrieve tweets given a tweet id
#https://api.twitter.com/1.1/statuses/lookup.json

from requests_oauthlib import OAuth1
import requests
import re
import json
import secret_data
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET
tweet_file = "tweet.json"
CACHE_FNAME = 'twitter_cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

# filename = 'training_set_1_ids.txt'
filename = 'test_tweet_ids.txt' #this is just a sub-set of tweet ids taken from 'training_set_1_ids.txt'

def read_in_tweet_ids():
    with open(filename, 'r') as infile:
        for line in infile:
            found_id = line.split('\t')[0]
            get_tweets(found_id)

def params_unique_combination(baseurl, params_diction):
    alphabetized_keys = sorted(params_diction.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params_diction[k]))
    return baseurl + "_" + "_".join(res)

def get_tweets(found_id):
    #https://api.twitter.com/1.1/statuses/lookup.json?id=20,432656548536401920
    base_url = 'https://api.twitter.com/1.1/statuses/lookup.json'
    params_diction = {'id': found_id}
    unique_ident = params_unique_combination(base_url, params_diction)

    # print(unique_ident)

    if unique_ident in CACHE_DICTION:
        print("\nGetting cached data...\n")
        return CACHE_DICTION[unique_ident]
    else:
        print("\nRetrieving from Twitter...\n")
        resp = requests.get(base_url, params_diction, auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

if __name__ == "__main__":
    check = read_in_tweet_ids()
import tweepy
import json
import secret_data

#Start getting keys & secrets for running Twitter user, you will need your own user with details saved in a file named 'secret_data.txt' to run this
CONSUMER_KEY = secret_data.CONSUMER_KEY
CONSUMER_SECRET = secret_data.CONSUMER_SECRET
ACCESS_TOKEN = secret_data.ACCESS_TOKEN
ACCESS_SECRET = secret_data.ACCESS_SECRET
#End getting keys & secrets for running Twitter user

#Start cache setup
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read() #this is a str
    CACHE_DICTION = json.loads(cache_contents) #this is a dict
    cache_file.close()
except:
    CACHE_DICTION = {}
#End cache setup

#Start OAuth code
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
#End OAuth code

FILENAME = 'test_tweet_ids.txt' #this is just a sub-set of tweet ids taken from 'training_set_1_ids.txt'

#Start cache check
def get_tweet(found_id):
    if found_id in CACHE_DICTION:
        return CACHE_DICTION[found_id]
    else:
        try:
            resp = api.get_status(found_id) #resp is a class 'tweepy.models.Status'
            json_str = json.dumps(resp._json) #json_str var is str type
            json_obj = json.loads(json_str) #json_obj var is dict type
        except:
            json_obj = {}
        CACHE_DICTION[found_id] = json_obj #creating new entry in cache dict where key = 'found_id' & value = 'json_obj' which is a dict
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # close the open file
        return CACHE_DICTION[found_id]
#End cache check

def read_in_tweet_ids():
    with open(FILENAME, 'r') as infile:
        for line in infile:
            found_id = line.split('\t')[0]
            try:
                get_tweet(found_id)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    check = read_in_tweet_ids()
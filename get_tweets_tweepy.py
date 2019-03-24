import tweepy
import json
import os
import secret_data
import sqlite3 as sql

# Start getting keys & secrets for running Twitter user, you will need your own user with details saved in a file named 'secret_data.txt' to run this
CONSUMER_KEY = secret_data.CONSUMER_KEY
CONSUMER_SECRET = secret_data.CONSUMER_SECRET
ACCESS_TOKEN = secret_data.ACCESS_TOKEN
ACCESS_SECRET = secret_data.ACCESS_SECRET
# End getting keys & secrets for running Twitter user

# Get current dir and train-data dir
curdir = os.curdir()
traindir = curdir + '/train-data'

#Start cache setup
# CACHE_FNAME = 'twitter_cache.json'
# try:
    # cache_file = open(CACHE_FNAME, 'r')
    # cache_contents = cache_file.read() #this is a str
    # CACHE_DICTION = json.loads(cache_contents) #this is a dict
    # cache_file.close()
# except:
    # CACHE_DICTION = {}
#End cache setup

# Start DB setup
DB_NAME = 'tweets.db'
create = str(input('Do you want to delete existing tables and recreate database? [y/n]: '))
if create.lower() == 'y':
    conn = sql.connect(DB_NAME)
    cur = conn.cursor()
    
    command = '''
        DROP TABLE IF EXISTS tweets
    '''
    
    cur.execute(command)
    conn.commit()
    
    command = '''
        CREATE TABLE tweets (
        id INTEGER PRIMARY KEY,
        tweepy_object BLOB
        )
    '''
    cur.execute(command)
    conn.commit()
    conn.close()

# Start OAuth code
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
# End OAuth code

FILENAME = 'test_tweet_ids.txt' #this is just a sub-set of tweet ids taken from 'training_set_1_ids.txt'

# Start cache check
# TODO: Rewrite w/ SQLite caching
# Requires: Valid ID for tweet
# Modifies: SQLite database
# Effects: If tweet has not been found before, extracts and saves tweepy object to database
#          If tweet has been found, extracts tweety object from database
#          Returns text body from tweepy object for file saving
def get_tweet(found_id):
    # if found_id in CACHE_DICTION:
        # return CACHE_DICTION[found_id]
    # else:
        # try:
            # resp = api.get_status(found_id) #resp is a class 'tweepy.models.Status'
            # json_str = json.dumps(resp._json) #json_str var is str type
            # json_obj = json.loads(json_str) #json_obj var is dict type
        # except:
            # json_obj = {}
        # CACHE_DICTION[found_id] = json_obj #creating new entry in cache dict where key = 'found_id' & value = 'json_obj' which is a dict
        # dumped_json_cache = json.dumps(CACHE_DICTION)
        # fw = open(CACHE_FNAME,"w")
        # fw.write(dumped_json_cache)
        # fw.close() # close the open file
        # return CACHE_DICTION[found_id]
    conn = sql.connect(DB_NAME)
    cur = conn.connect()
    
    command = '''
        SELECT EXISTS(SELECT 1 FROM tweets WHERE id = ?)
    '''
    cur.execute(command, (found_id,))
    exists = cur.fetchone()[0]
    
    if exists:
        command = '''
            SELECT tweepy_object FROM tweets WHERE id = ?
        '''
        cur.execute(command, (found_id,))
        text = cur.fetchone()[0].text
    else:
        resp = api.get_status(found_id)
        command = '''
            INSERT INTO tweets (id, tweepy_object) VALUES (?, ?)
        '''
        cur.execute(command, (found_id, resp))
        text = resp.text
    
    conn.commit()
    conn.close()
    return text
# End cache check

# TODO: save to aformentioned train-data structure
# HINT: Use os.path.isfile(file) to check if file already exists
# Requires: Valid filename for tweet IDs be a global var
# Modifies: train-data directory and subdirectories
# Effects: Finds tweets by ID using tweepy; saves tweet text to dir structure for sklearn
def read_in_tweet_ids():
    with open(FILENAME, 'r') as infile:
        for line in infile:
            found_id = line.split('\t')[0]
            found_mention = line.split('\t')[2]
            dir = traindir + '/%s' % (found_mention)
            file = dir + '/%s.txt' % (found_id)
            try:
                if not os.path.isfile(file):
                    text = get_tweet(found_id)
                    f = open(file, 'w')
                    f.write(text)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    check = read_in_tweet_ids()
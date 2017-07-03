import oauth2 as oauth
import time
import json
import config as cfg
import csv

#twitter API
consumer = oauth.Consumer(key=cfg.twitter['CONSUMER_KEY'], secret=cfg.twitter['CONSUMER_SECRET'])
access_token = oauth.Token(key=cfg.twitter['ACCESS_KEY'], secret=cfg.twitter['ACCESS_SECRET'])
client = oauth.Client(consumer, access_token)

#import ids from csv
ids=[]

idsfile = open("data/ids/tweet.csv", 'r')
spamreader = csv.reader(idsfile, delimiter=' ', quotechar='"')
for id in spamreader:
    ids.append(id[0])

print(len(ids)," tweets to retrieve")

#retrieve json from twitter API
jsonfile = open("data/json/tweet.json", 'w')
while len(ids) > 0:
        parameter = ','.join(ids[0:99]) #max 100 id per request
        ids[0:99] = []
        try:
            place_endpoint = "https://api.twitter.com/1.1/statuses/lookup.json?id="+parameter
            response, data = client.request(place_endpoint)
            if response['status'] == '200':
                if int(response['x-rate-limit-remaining'])<2:
                    print('id rescue: wait '+str(int(response['x-rate-limit-reset']) - int(time.time()))+' seconds')
                    time.sleep(int(response['x-rate-limit-reset'])-int(time.time()))

            jsonTweet = json.loads(data.decode("utf-8"))
            for tweet in jsonTweet:
                jsonfile.write(json.dumps(tweet)+"\n")

            print('id rescue: wait '+str((15*60)/int(response['x-rate-limit-limit']))+' seconds')
            time.sleep((15*60)/int(response['x-rate-limit-limit']))
        except Exception as err:
            print("OS error: {0}".format(err))

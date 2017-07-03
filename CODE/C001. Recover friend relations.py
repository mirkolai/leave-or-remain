import oauth2 as oauth
import time
import json
import config as cfg
import pymysql
import sys

#twitter API
consumer = oauth.Consumer(key=cfg.twitter['CONSUMER_KEY'], secret=cfg.twitter['CONSUMER_SECRET'])
access_token = oauth.Token(key=cfg.twitter['ACCESS_KEY'], secret=cfg.twitter['ACCESS_SECRET'])
client = oauth.Client(consumer, access_token)

db = pymysql.connect(host=cfg.mysql['host'], # your host, usually localhost
             user=cfg.mysql['user'], # your username
             passwd=cfg.mysql['passwd'], # your password
             db=cfg.mysql['db'],
             charset='utf8') # name of the data base

cur = db.cursor()
cur.execute('SET NAMES utf8mb4')
cur.execute("SET CHARACTER SET utf8mb4")
cur.execute("SET character_set_connection=utf8mb4")
db.commit()

cur.execute("SELECT  `screen_name`,user_id FROM `user` WHERE  `phase_1`>=3 and `phase_2`>=3 and `phase_3` >=3 and user_id not in (select distinct source from user_friends_relation)")
users=cur.fetchall()
i=len(users)
for user in users:
    i-=1
    print(str(i))
    next_cursor=-1
    while next_cursor!=0:

        if next_cursor<0:
            timeline_endpoint = "https://api.twitter.com/1.1/friends/ids.json?count=5000&cursor=-1&screen_name="+str(user[0])+"&skip_status=true&include_user_entities=true"
            print(timeline_endpoint)

        else:
            timeline_endpoint = "https://api.twitter.com/1.1/friends/ids.json?count=5000&cursor="+str(next_cursor)+"&screen_name="+str(user[0])+"&skip_status=true&include_user_entities=true"
            print(timeline_endpoint)
        try:
            response, data = client.request(timeline_endpoint)
            print(response)
            print(data)

            if response['status']=='200':
                if int(response['x-rate-limit-remaining'])<2:
                    print('id rescue: wait '+str(int(response['x-rate-limit-reset'])-int(time.time()))+' seconds')
                    time.sleep(int(response['x-rate-limit-reset'])-int(time.time()))

                dataResult = json.loads(data.decode("utf-8"))

                next_cursor = dataResult['next_cursor']

                for userFollower in dataResult['ids']:
                    print(userFollower)
                    cur.execute(" INSERT INTO `user_friends_relation`(`source`, `target`) "
                                " values "
                                " (%s,%s) on duplicate key update source=source",
                    (user[1],userFollower))

                print('id rescue: wait '+str((15*60)/int(response['x-rate-limit-limit']))+' seconds')
                time.sleep((15*60)/int(response['x-rate-limit-limit']))



            elif response['status']=='400' or response['status']=='403' or response['status']=='404' or response['status']=='401':
                print(response['status'])
                next_cursor=0
            elif  response['status']=='429':
                print(response['status'])
                next_cursor=-1
                print('id rescue: wait '+str(int(response['x-rate-limit-reset'])-int(time.time()))+' seconds')
                time.sleep(int(response['x-rate-limit-reset'])-int(time.time()))
            else:
                print(response['status'])
                next_cursor=0

        except:
            e = sys.exc_info()[0]
            print('exeption '+e)
            time.sleep(60)
            continue

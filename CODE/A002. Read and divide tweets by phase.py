# -*- coding: utf-8 -*-
import pytz
import pymysql
import json
import config as cfg
from datetime import datetime

#import data/database_structure/leave_or_remain.sql

#connet # to mysql
db = pymysql.connect(host=cfg.mysql['host'],
                    user=cfg.mysql['user'],
                    passwd=cfg.mysql['passwd'],
                    db=cfg.mysql['db'],
                    charset='utf8')

cur = db.cursor()
cur.execute('SET NAMES utf8mb4')
cur.execute("SET CHARACTER SET utf8mb4")
cur.execute("SET character_set_connection=utf8mb4")
db.commit()

#read json file and save tweets on mysql

infile = open("data/json/tweet.json", 'r')

for row in infile:
    data = json.loads(row)

    if data['lang']=='en':

        date=datetime.strptime(data['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)


        if not data.get('retweeted_status'):
            retweet=0
            text=data['text'].lower()
        else:
            retweet=1
            text=data['retweeted_status']['text'].lower()

        if data['in_reply_to_status_id'] is None:
            reply=0
        else:
            reply=data['in_reply_to_status_id']


        phase=0
        if date > datetime(2016, 6, 22, 22, 0, 0, 0).replace(tzinfo=pytz.UTC)  and date < datetime(2016, 6, 23, 22, 0, 0, 0).replace(tzinfo=pytz.UTC):
            phase=1
        elif date > datetime(2016, 6, 24, 8, 0, 0, 0).replace(tzinfo=pytz.UTC) and date < datetime(2016, 6, 25, 8, 0, 0, 0).replace(tzinfo=pytz.UTC):
            phase = 2
        elif date > datetime(2016, 6, 28, 0, 0, 0, 0).replace(tzinfo=pytz.UTC) and date < datetime(2016, 6, 29, 0, 0, 0, 0).replace(tzinfo=pytz.UTC):
            phase=3

        print(date)

        if phase!=0:
            cur.execute(" INSERT INTO `tweet_phase`(`id`, `user_id`,`screen_name`, `text`, `date`, `phase`, `retweet`, `reply`) "
                        " VALUES (%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key  update id=id",
            (data['id'],
             data['user']['id'],
             data['user']['screen_name'],
             text,
             date.strftime("%Y-%m-%d %H:%M:%S"),
             phase,
             retweet,
             reply
            ))
            db.commit()




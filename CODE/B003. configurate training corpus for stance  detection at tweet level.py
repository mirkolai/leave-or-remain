# -*- coding: utf-8 -*-
import pytz
import gzip
import os
import pymysql
import json
import config as cfg
import glob
from datetime import datetime

print(os.getcwd())

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


cur.execute("SELECT `phase`, `tweet_id_1`, `tweet_id_2`, `tweet_id_3`, `text_1`, `text_2`, `text_3`, `stance` FROM `sample_1_row_stance_confidence` where confidence > 0.6")
tweets=cur.fetchall()
for tweet in tweets:
    phase = tweet[0]
    tweet_id_1 = tweet[1]
    tweet_id_2 = tweet[2]
    tweet_id_3 = tweet[3]
    tweet_text_1 = tweet[4]
    tweet_text_2 = tweet[5]
    tweet_text_3 = tweet[6]
    stance = tweet[7]

    if stance=="leave":
        stance=-1
    elif stance=="remain":
        stance=1
    else:
       stance=0

    cur.execute(" INSERT INTO `sample_1_training_corpus`"
                " (`id`, `text`, `phase`, `stance`) "
                " VALUES  "
                " (%s,%s,%s,%s) ",
                (tweet_id_1, tweet_text_1,phase,stance))

    cur.execute(" INSERT INTO `sample_1_training_corpus`"
                " (`id`, `text`, `phase`, `stance`) "
                " VALUES  "
                " (%s,%s,%s,%s) ",
                (tweet_id_2, tweet_text_2,phase,stance))

    cur.execute(" INSERT INTO `sample_1_training_corpus`"
                " (`id`, `text`, `phase`, `stance`) "
                " VALUES  "
                " (%s,%s,%s,%s) ",
                (tweet_id_3, tweet_text_3,phase,stance))

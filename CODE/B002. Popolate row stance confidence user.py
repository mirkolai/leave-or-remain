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


cur.execute("SELECT distinct `user_id` FROM `sample_1_row` ")
users=cur.fetchall()
for user in users:
    user_id=user[0]
    cur.execute("SELECT stance FROM `sample_1_row_stance_confidence` WHERE user_id=%s order by phase asc",(user_id))
    tweet=cur.fetchall()

    stance_1=tweet[0][0]
    stance_2=tweet[1][0]
    stance_3=tweet[2][0]

    cur.execute(" INSERT INTO `sample_1_row_stance_confidence_user` "
                " (`user_id`, `stance_1`, `stance_2`, `stance_3`)"
                " VALUES "
                " (%s,%s,%s,%s) ",
                (user_id, stance_1,stance_2,stance_3))

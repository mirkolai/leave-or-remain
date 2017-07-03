# -*- coding: utf-8 -*-
import pymysql
import config as cfg

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


cur.execute("SELECT `user_id`, `screen_name`,`phase` FROM `tweet_phase`")
tweets=cur.fetchall()

for tweet in tweets:
    user_id=tweet[0]
    user_screen_name=tweet[1]
    phase=tweet[2]

    phase_0=0
    phase_1=0
    phase_2=0
    phase_3=0

    if  phase==1 :
        phase_1 = 1
    elif phase==2:
        phase_2 = 1
    elif phase==3:
        phase_3 = 1
    else:
        phase_0 = 1


    cur.execute(" INSERT INTO `user`(`user_id`, `screen_name`, `phase_1`, `phase_2`, `phase_3`)"
                " VALUES (%s,%s,%s,%s,%s) on duplicate key update  `phase_1`=`phase_1`+%s,"
                " `phase_2`=`phase_2`+%s, `phase_3`=`phase_3`+%s",
    ( user_id,
      user_screen_name,
      phase_1,
      phase_2,
      phase_3,
      phase_1,
      phase_2,
      phase_3
    ))
    db.commit()




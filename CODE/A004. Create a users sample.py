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

cur.execute("SELECT `user_id`, `screen_name`,`phase_1`, `phase_2`, `phase_3` FROM `user` where `phase_1`>=3 and `phase_2`>=3 and `phase_3`>=3 order by rand()")
tweets=cur.fetchall()
for tweet in tweets[0:600]:
    user_id=tweet[0]
    user_screen_name=tweet[1]
    phase_1=tweet[2]
    phase_2=tweet[3]
    phase_3=tweet[4]



    cur.execute(" INSERT INTO `sample_1_user_selected`"
                "(`user_id`, `screen_name`, `phase_1`, `phase_2`, `phase_3`) "
                "VALUES (%s,%s,%s,%s,%s)",
    ( user_id,
      user_screen_name,
      phase_1,
      phase_2,
      phase_3
    ))
    db.commit()




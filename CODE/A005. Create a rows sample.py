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

cur.execute("SELECT `user_id` FROM `sample_1_user_selected`")
users=cur.fetchall()
for user in users:
    user_id=user[0]
    for phase in [1,2,3]:
        cur.execute("SELECT `id`,`text` FROM `tweet_phase` WHERE user_id=%s and phase=%s order by rand()",(user_id,phase))
        tweets=cur.fetchall()

        print(tweets)

        for index in [0]:
            tweet_id_1=tweets[0+(index*3)][0]
            tweet_text_1=tweets[0+(index*3)][1]

            tweet_id_2=tweets[1+(index*3)][0]
            tweet_text_2=tweets[1+(index*3)][1]

            tweet_id_3=tweets[2+(index*3)][0]
            tweet_text_3=tweets[2+(index*3)][1]

            cur.execute(" INSERT INTO `sample_1_row` "
                        " (`user_id`, `phase`, `index`, `tweet_id_1`, `tweet_id_2`, `tweet_id_3`, `text_1`, `text_2`, `text_3`) "
                        " VALUES "
                        " (%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(user_id,phase,index,tweet_id_1,tweet_id_2,tweet_id_3,tweet_text_1,tweet_text_2,tweet_text_3))





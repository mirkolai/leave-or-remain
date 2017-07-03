# -*- coding: utf-8 -*-
import os
import pymysql
import config as cfg


# import data/annotated_corpus/sample_1_crowdflower_aggregate.csv
print(os.getcwd())

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

cur.execute("SELECT  `what_is_the_stance_of_the_user_that_wrote_those_three_messages`, `what_is_the_stance_of_the_user:confidence`, `content`, `ids`, `_trusted_judgments` FROM `sample_1_crowdflower_aggregate` where `_golden`='false'")
rows=cur.fetchall()
for row in rows:
    ids=row[3].split("_")
    stance=row[0]
    confidence=row[1]
    contributors=row[4]
    cur.execute("SELECT `user_id`, `phase`, `index`, `tweet_id_1`, `tweet_id_2`, `tweet_id_3`, `text_1`, `text_2`, `text_3` FROM `sample_1_row` WHERE `tweet_id_1`=%s and  `tweet_id_2`=%s  and `tweet_id_3`=%s",(ids[0],ids[1],ids[2]))
    tweet=cur.fetchone()
    user_id=tweet[0]
    phase=tweet[1]
    index=tweet[2]
    tweet_id_1=tweet[3]
    tweet_id_2=tweet[4]
    tweet_id_3=tweet[5]
    tweet_text_1=tweet[6]
    tweet_text_2=tweet[7]
    tweet_text_3=tweet[8]

    if confidence<0.6:
        stance="NOTAGREEMENT"

    cur.execute("INSERT INTO `sample_1_row_stance_confidence`"
                    "(`user_id`, `phase`, `index`, `tweet_id_1`, `tweet_id_2`, `tweet_id_3`, `text_1`, `text_2`, `text_3`, `stance`, `confidence`, `contributors`) "
                    "VALUES "
                    " (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",(user_id,phase,index,tweet_id_1,tweet_id_2,tweet_id_3,tweet_text_1,tweet_text_2,tweet_text_3,stance,confidence,contributors))





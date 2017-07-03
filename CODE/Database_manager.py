from sklearn.externals import joblib
from Tweet import make_tweet
import os.path
import pymysql
import config as cfg

class Database_manager(object):

    db=None
    cur=None

    def __init__(self):

        self.db = pymysql.connect(host=cfg.mysql['host'],
                 user=cfg.mysql['user'],
                 passwd=cfg.mysql['passwd'],
                 db=cfg.mysql['db'],
                 charset='utf8')
        self.cur = self.db.cursor()
        self.cur.execute('SET NAMES utf8mb4')
        self.cur.execute("SET CHARACTER SET utf8mb4")
        self.cur.execute("SET character_set_connection=utf8mb4")
        self.db.commit()

    def return_tweets(self):


        if os.path.isfile('tweets_sample_1_task_a.pkl') :
            tweets= joblib.load('tweets_sample_1_task_a.pkl')
            return tweets


        tweets=[]
        self.cur.execute(" SELECT `sample_1_training_corpus`.`id`, `sample_1_training_corpus`.`text`, `sample_1_training_corpus`.`phase`, `sample_1_training_corpus`.`stance`, `tweet`.user_id "
                         " FROM `sample_1_training_corpus` "
                         " left join `tweet`  "
                         " on `tweet`.id = `sample_1_training_corpus`.id ")
        i=0
        not_founds=0
        for tweet in self.cur.fetchall():
                i+=1
                print(i,not_founds)
                id=tweet[0]
                text=tweet[1]
                phase=tweet[2]
                stance=tweet[3]
                user_id=tweet[4]
                self.cur.execute("SELECT community FROM `user_friends_relation_communities` where id=%s",(user_id))
                result=self.cur.fetchone()
                if result is not None:
                    community=result[0]
                else:
                    community=-1
                    not_founds+=1
                    print(id,user_id)


                this_tweet=make_tweet(id, text,phase, stance, community )

                tweets.append(this_tweet)

        joblib.dump(tweets, 'tweets_sample_1_task_a.pkl')

        return tweets


    def return_tweets_by_phase(self,phase):


        if os.path.isfile('tweets_sample_1_task_b_phase_'+str(phase)+'.pkl') :
            tweets= joblib.load('tweets_sample_1_task_b_phase_'+str(phase)+'.pkl')
            return tweets


        tweets=[]
        self.cur.execute(" SELECT `sample_1_training_corpus`.`id`, `sample_1_training_corpus`.`text`, `sample_1_training_corpus`.`phase`, `sample_1_training_corpus`.`stance`, `tweet`.user_id "
                         " FROM `sample_1_training_corpus` "
                         " left join `tweet`  "
                         " on `tweet`.id = `sample_1_training_corpus`.id "
                         " where phase =%s", (phase))
        i=0
        not_founds=0
        for tweet in self.cur.fetchall():
                i+=1
                print(i,not_founds)
                id=tweet[0]
                text=tweet[1]
                phase=tweet[2]
                stance=tweet[3]
                user_id=tweet[4]
                self.cur.execute("SELECT community FROM `user_friends_relation_communities` where id=%s",(user_id))
                result=self.cur.fetchone()
                if result is not None:
                    community=result[0]
                else:
                    community=-1
                    not_founds+=1
                    print(id,user_id)


                this_tweet=make_tweet(id, text,phase, stance, community )

                tweets.append(this_tweet)

        joblib.dump(tweets, 'tweets_sample_1_task_b_phase_'+str(phase)+'.pkl')

        return tweets

    def return_tweets_by_row(self):


        if os.path.isfile('tweets_sample_1_task_c.pkl') :
            tweets= joblib.load('tweets_sample_1_task_c.pkl')
            return tweets


        tweets=[]
        self.cur.execute("SELECT sample.`id_1`, sample.`text_1`, sample.`text_2`, sample.`text_3`, sample.`phase`, sample.`stance`, `tweet`.user_id "
                         " FROM `sample_1_training_corpus_for_user` as sample "
                         " left join `tweet`  "
                         " on `tweet`.id = sample.id_1 ")

        i=0
        not_founds=0
        for tweet in self.cur.fetchall():
                i+=1
                print(i,not_founds)
                id=tweet[0]
                text=tweet[1]+" "+tweet[2]+" "+tweet[3]
                phase=tweet[4]
                stance=tweet[5]
                user_id=tweet[6]
                self.cur.execute("SELECT community FROM `user_friends_relation_communities` where id=%s",(user_id))
                result=self.cur.fetchone()
                if result is not None:
                    community=result[0]
                else:
                    community=-1
                    not_founds+=1
                    print(id,user_id)


                this_tweet=make_tweet(id, text,phase, stance, community )

                tweets.append(this_tweet)

        joblib.dump(tweets, 'tweets_sample_1_task_c.pkl')

        return tweets




def make_database_manager():
    database_manager = Database_manager()

    return database_manager





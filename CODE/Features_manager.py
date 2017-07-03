from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import re
from scipy.sparse import csr_matrix, hstack



class Features_manager(object):

    def __init__(self):


        return

    def get_stance(self,tweets):

        stance  = []

        for tweet in tweets:
            stance.append(tweet.stance)


        return stance


    #features extractor
    def create_feature_space(self,tweets,featureset):


        global_featureset={
            "BoW"  : self.get_BoW_features(tweets),
            "hashtag" : self.get_hashtag_features(tweets),
            "numhashtag" : self.get_numhashtag_features(tweets),
            "mention"  : self.get_mention_features(tweets),
            "nummention"  : self.get_nummention_features(tweets),
            "sentiment_afinn" : self.get_sentiment_afinn_features(tweets),
            "sentiment_liwc" : self.get_sentiment_LIWC_features(tweets),
            "sentiment_hl" : self.get_sentiment_HL_features(tweets),
            "sentiment_dal" : self.get_sentiment_DAL_features(tweets),
            "punctuation_marks": self.get_puntuaction_marks_features(tweets),
            "phase": self.get_phase_features(tweets),
            "community": self.get_community_features(tweets),
            "target":self.get_target_features(tweets),
            "parties_knowledge": self.get_parties_knowledge_features(tweets),
            "politics_knowledge": self.get_politics_knowledge_features(tweets),

        }

        all_feature_names=[]
        all_feature_index=[]
        all_X=[]
        index=0
        for key in featureset:
            X,feature_names=global_featureset[key]

            current_feature_index=[]
            for i in range(0,len(feature_names)):
                current_feature_index.append(index)
                index+=1
            all_feature_index.append(current_feature_index)

            all_feature_names=np.concatenate((all_feature_names,feature_names))
            if all_X!=[]:
                all_X=csr_matrix(hstack((all_X,X)))
            else:
                all_X=X

        return all_X, all_feature_names, np.array(all_feature_index)

    def get_BoW_features(self, tweets):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,3),
                                          stop_words="english",
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)

        feature  = []
        for tweet in tweets:

            feature.append(tweet.text)


        tfidfVectorizer = tfidfVectorizer.fit(feature)

        X = tfidfVectorizer.transform(feature)

        feature_names=tfidfVectorizer.get_feature_names()

        return X, feature_names

    def get_hashtag_features(self, tweets, train_tweets=None):


        tfidfVectorizer = CountVectorizer(ngram_range=(1,1),
                                          #stop_words="english",
                                          lowercase=False, #true 0.507 false 0.51
                                          binary=True,
                                          max_features=500000)

        feature  = []
        for tweet in tweets:
            feature.append(' '.join(re.findall(r"#(\w+)", tweet.text)))



        tfidfVectorizer = tfidfVectorizer.fit(feature)

        X = tfidfVectorizer.transform(feature)

        feature_names=tfidfVectorizer.get_feature_names()


        return X, feature_names

    def get_numhashtag_features(self, tweets):

        feature  = []

        for tweet in tweets:
            feature.append(len(re.findall(r"#(\w+)", tweet.text)))




        return csr_matrix(np.vstack(feature)),["feature_numhashtag"]

    def get_mention_features(self, tweets):


        tfidfVectorizer = CountVectorizer(ngram_range=(1,1),
                                          #stop_words="english",
                                          lowercase=False, #true 0.507 false 0.51
                                          binary=True,
                                          max_features=500000)

        feature  = []
        for tweet in tweets:
            feature.append(' '.join(re.findall(r"@(\w+)", tweet.text)))


        tfidfVectorizer = tfidfVectorizer.fit(feature)

        X = tfidfVectorizer.transform(feature)

        feature_names=tfidfVectorizer.get_feature_names()


        return X, feature_names

    def get_nummention_features(self, tweets):

        feature  = []

        for tweet in tweets:
            feature.append(len(re.findall(r"@(\w+)", tweet.text)))


        return csr_matrix(np.vstack(feature)),["feature_nummention"]

    def get_sentiment_afinn_features(self,tweets):

        sentiment  = []

        for tweet in tweets:

            sentiment.append(tweet.sentimentafinn)


        return csr_matrix(np.vstack(sentiment)),["feature_sentiment_afinn"]

    def get_sentiment_LIWC_features(self,tweets):

        sentiment  = []

        for tweet in tweets:

            sentiment.append(tweet.sentimentliwc)



        return csr_matrix(np.vstack(sentiment)),["feature_sentiment_liwc"]

    def get_sentiment_HL_features(self,tweets):

        sentiment  = []

        for tweet in tweets:

            sentiment.append(tweet.sentimenthl)



        return csr_matrix(np.vstack(sentiment)),["feature_sentiment_HL"]

    def get_sentiment_DAL_features(self,tweets):

        sentiment  = []

        for tweet in tweets:

            sentiment.append(tweet.sentimentdal)


        return csr_matrix(np.vstack(sentiment)),["feature_sentiment_dal_pleasantness", "feature_sentiment_dal_activation", "feature_sentiment_dal_imagery"]



    def get_puntuaction_marks_features(self,tweets):

        feature  = []

        for tweet in tweets:
            feature.append([
                len(re.findall(r"[!]", tweet.text)),
                len(re.findall(r"[?]", tweet.text)),
                len(re.findall(r"[.]", tweet.text)),
                len(re.findall(r"[,]", tweet.text)),
                len(re.findall(r"[;]", tweet.text)),
                len(re.findall(r"[!?.,;]", tweet.text)),
                ]

            )


        return csr_matrix(np.vstack(feature)),["feature_numhashtag"]

    def get_phase_features(self,tweets):

        phase  = []

        for tweet in tweets:
            feature=[0,0,0]
            feature[tweet.phase-1]=1
            phase.append(feature)


        return csr_matrix(np.vstack(phase)),["feature_phase_1","feature_phase_2","feature_phase_3"]



    def get_community_features(self, tweets):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,1),
                                          lowercase=True,
                                          binary=True,
                                          max_features=500000)

        feature  = []
        for tweet in tweets:
            feature.append("feature_community_"+str(tweet.community).replace("-","menus_"))


        tfidfVectorizer = tfidfVectorizer.fit(feature)

        X = tfidfVectorizer.transform(feature)

        feature_names=tfidfVectorizer.get_feature_names()
        return X, feature_names

    def get_target_features(self,tweets):

        phase  = []

        for tweet in tweets:
            is_leave=0
            is_remain=0
            alias_leave=["leave"]
            alias_remain=["remain"]
            for alias in alias_leave:
                if alias in tweet.text.lower():
                    is_leave=1
            for alias in alias_remain:
                if alias in tweet.text.lower():
                    is_remain=1

            phase.append([is_leave,is_remain])


        return csr_matrix(np.vstack(phase)),["feature_target_leave","feature_target_remain"]

    def get_politics_knowledge_features(self, tweets):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,1),
                                          #stop_words="english",
                                          #lowercase=True,
                                          binary=True,
                                          max_features=500000)

        feature  = []
        for tweet in tweets:

            feature.append(tweet.text_politic_alias)


        tfidfVectorizer = tfidfVectorizer.fit(feature)

        X = tfidfVectorizer.transform(feature)

        feature_names=tfidfVectorizer.get_feature_names()

        return X, feature_names

    def get_parties_knowledge_features(self, tweets):

        tfidfVectorizer = CountVectorizer(ngram_range=(1,1),
                                          #stop_words="english",
                                          #lowercase=True,
                                          binary=True,
                                          max_features=500000)

        feature  = []
        for tweet in tweets:

            feature.append(tweet.text_parties_alias)


        tfidfVectorizer = tfidfVectorizer.fit(feature)

        X = tfidfVectorizer.transform(feature)

        feature_names=tfidfVectorizer.get_feature_names()

        return X, feature_names



#inizializer
def make_feature_manager():

    features_manager = Features_manager()

    return features_manager


from Linguistic_resource_LIWC import LIWC
from Linguistic_resource_AFINN import AFINN
from Linguistic_resource_DAL import DAL
from Linguistic_resource_HL import HL
from Linguistic_resource_wordlist import WORDLIST
from Semantic_resource_dbpedia import DBPEDIA

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

porter_stemmer = PorterStemmer()


liwc = LIWC()
afinn = AFINN()
dal = DAL()
hl = HL()
wordlist = WORDLIST()
dbpedia = DBPEDIA()


class Tweet(object):

    tweet_id=0
    text=''
    phase=-1
    stance=0 #-1 leave 0 untellige 1 remain
    community=-1

    def __init__(self, tweet_id, text, phase, stance, community):



        text=text.replace("#brexit"," ")

        self.tweet_id=tweet_id

        self.text=re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' URL ', text)
        self.text_no_stop_word=" ".join([word for word in self.text if word not in stopwords.words('english')])
        self.text_hashtag_and_screen_name_slitted=wordlist.ParseSentence(self.text)

        self.tokens = nltk.word_tokenize(self.text_hashtag_and_screen_name_slitted)
        self.tokens_sentiment = hl.get_HL_sentiment_tokens(self.tokens)
        self.lemmas = [ porter_stemmer.stem(token) for token in self.tokens]
        self.pos = [ token[1] for token in nltk.pos_tag(self.tokens)]

        self.sentimentafinn=afinn.get_afinn_sentiment(text)
        self.sentimentdal=dal.get_dal_sentiment(text)
        self.sentimenthl=hl.get_HL_sentiment(text)
        self.sentimentliwc=liwc.get_liwc_sentiment(text)

        self.liwc_text=liwc.get_liwc_text(self.tokens)
        self.liwc_function=liwc.get_liwc_functions(self.tokens)


        self.phase=phase
        self.stance=stance
        self.community=community

        self.text_politic_alias = dbpedia.replace_politics_alias_with_stance(text)
        self.text_parties_alias = dbpedia.replace_parties_alias_with_stance(text)




def make_tweet(tweet_id, text, phase, stance, community=-1):

    tweet = Tweet(tweet_id, text, phase, stance, community)

    return tweet




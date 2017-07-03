class DBPEDIA(object):


    def __init__(self):

        self.Semantic_resource={}

        file = 'resources/Semantic_resource_parties_LEAVE.txt'
        with open(file) as f:
            content = f.readlines()
        self.Semantic_resource["parties_LEAVE"] = [word.lower().rstrip('\n') for word in content]

        file = 'resources/Semantic_resource_parties_REMAIN.txt'
        with open(file) as f:
            content = f.readlines()
        self.Semantic_resource["parties_REMAIN"] = [word.lower().rstrip('\n') for word in content]

        file = 'resources/Semantic_resource_parties_NEUTRAL.txt'
        with open(file) as f:
            content = f.readlines()
        self.Semantic_resource["parties_NEUTRAL"] = [word.lower().rstrip('\n') for word in content]

        file = 'resources/Semantic_resource_politics_LEAVE.txt'
        with open(file) as f:
            content = f.readlines()
        self.Semantic_resource["politics_LEAVE"] = [word.lower().rstrip('\n') for word in content]

        file = 'resources/Semantic_resource_politics_REMAIN.txt'
        with open(file) as f:
            content = f.readlines()
        self.Semantic_resource["politics_REMAIN"] = [word.lower().rstrip('\n') for word in content]

        file = 'resources/Semantic_resource_politics_NEUTRAL.txt'
        with open(file) as f:
            content = f.readlines()
        self.Semantic_resource["politics_NEUTRAL"] = [word.lower().rstrip('\n') for word in content]


        return



    def replace_politics_alias_with_stance(self, sentence):

        result_sentence=""

        for key  in self.Semantic_resource:
            if "politics" in key:
                for alias in self.Semantic_resource[key]:
                    if alias in sentence:
                        result_sentence+=" feature_presence_alias_"+key+""


        if result_sentence=="":
            result_sentence="feature_presence_alias_NO_ALIAS"

        return result_sentence

    def replace_parties_alias_with_stance(self, sentence):

        result_sentence=""

        for key  in self.Semantic_resource:
            if "parties" in key:
                for alias in self.Semantic_resource[key]:
                    if alias in sentence:
                        result_sentence+=" feature_presence_alias_"+key+""


        if result_sentence=="":
            result_sentence="feature_presence_alias_NO_ALIAS"

        return result_sentence




if __name__ == '__main__':

    sentence="tweet content"
    dbpedia=DBPEDIA()

    result=dbpedia.replace_parties_alias_with_stance(sentence.lower())
    print(result)

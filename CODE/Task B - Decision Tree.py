from sklearn.tree.tree import DecisionTreeClassifier
import Features_manager
import Database_manager
from itertools import combinations
from sklearn.metrics.classification import precision_recall_fscore_support, accuracy_score
import config_features as cfg_feature
from sklearn.cross_validation import KFold
import numpy


print("Task B - Decision Tree")


database_manager=Database_manager.make_database_manager()
feature_manager=Features_manager.make_feature_manager()

file = open("Task B - Decision Tree.csv","w")

for phase in [1,2,3]:
    tweets=numpy.array(database_manager.return_tweets_by_phase(phase))
    stance=numpy.array(feature_manager.get_stance(tweets))


    feature_names=cfg_feature.feature_list['feature_names']


    feature_names=numpy.array([["BoW"],
                   ["hashtag","numhashtag","mention","nummention","punctuation_marks"],
                   ["sentiment_afinn", "sentiment_liwc","sentiment_hl","sentiment_dal"],
                   ["phase"],
                   ["community"],
                   ["parties_knowledge","politics_knowledge","target"]])


    stuff = range(0, len(feature_names) )

    max=0
    for L in range(1, len(stuff)+1):
        for subset in combinations(stuff, L):


            feature_filtered=numpy.concatenate(feature_names[list(subset)])
            print(feature_filtered)

            X,feature_name_global,feature_index_global=feature_manager.create_feature_space(tweets,feature_filtered)
            fmacros_average=[]
            for i in range(0,10):

                print(i,feature_filtered)

                #5 cross validation over current feature set combination
                fmacros=[]
                kf = KFold(len(tweets),n_folds=5, random_state=True)
                for index_train, index_test in kf:

                    X_train=X[index_train]
                    X_test=X[index_test]


                    clf = DecisionTreeClassifier()

                    clf.fit(X_train.toarray(),stance[index_train])
                    test_predict = clf.predict(X_test.toarray())

                    prec, recall, f, support = precision_recall_fscore_support(
                    stance[index_test],
                    test_predict,
                    beta=1)

                    accuracy = accuracy_score(
                    stance[index_test],
                    test_predict
                    )

                    fmacros.append(((f[0]+f[2])/2))

                fmacros_average.append(numpy.average(fmacros))

            file.write('"'+(' '.join(feature_filtered))+'"'+'\t'+str(phase)+'\t'+str(numpy.average(fmacros_average))+'\t'+str(X.shape)+'\n')
            print('"'+(' '.join(feature_filtered))+'"'+'\t'+str(phase)+'\t'+str(numpy.average(fmacros_average))+'\n')
            if numpy.average(fmacros) >max:
                max= numpy.average(fmacros)
                print("MAX:"+(' '.join(feature_filtered))+" "+str(max))
file.close()

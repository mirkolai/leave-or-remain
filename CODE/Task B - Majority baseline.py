from collections import Counter
import numpy
import Features_manager
import Database_manager
from sklearn.metrics.classification import precision_recall_fscore_support, accuracy_score
from sklearn.cross_validation import KFold


print("Task B - Majority baseline")


database_manager=Database_manager.make_database_manager()
feature_manager=Features_manager.make_feature_manager()
file = open("Task B - Majority baseline.csv","w")

for phase in [1,2,3]:

    tweets=numpy.array(database_manager.return_tweets_by_phase(phase=phase))
    stance=numpy.array(feature_manager.get_stance(tweets))

    fmacros=[]
    max=0
    kf = KFold(len(tweets),n_folds=5, random_state=True)
    for index_train, index_test in kf:

        count = Counter(stance[index_train])
        print(count.most_common())
        majority_class=count.most_common()[0][0]
        test_predict = [majority_class]*len(stance[index_test])
        prec, recall, f, support = precision_recall_fscore_support(
        stance[index_test],
        test_predict,
        beta=1)
        accuracy = accuracy_score(
        stance[index_test],
        test_predict
        )

        print(prec, recall, f, support,accuracy)

        fmacros.append(((f[0]+f[2])/2))


    file.write('"Majority Baseline"'+'\t'+str(numpy.average(fmacros))+'\t'+str(phase)+'\n')

    if numpy.average(fmacros) >max:
        max= numpy.average(fmacros)
        print("MAX:"+'"Majority Baseline"'+" "+str(max))

file.close()
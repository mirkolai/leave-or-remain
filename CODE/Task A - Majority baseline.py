from collections import Counter
import numpy
import Features_manager
import Database_manager
from sklearn.metrics.classification import precision_recall_fscore_support, accuracy_score
from sklearn.cross_validation import KFold


print("Task A - Majority baseline")


database_manager=Database_manager.make_database_manager()
feature_manager=Features_manager.make_feature_manager()

tweets=numpy.array(database_manager.return_tweets())
stance=numpy.array(feature_manager.get_stance(tweets))

file = open("Task A - Majority baseline.csv","w")


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


file.write('"Majority Baseline"'+'\t'+str(numpy.average(fmacros))+'\n')

if numpy.average(fmacros) >max:
    max= numpy.average(fmacros)
    print("MAX:"+'"Majority Baseline"'+" "+str(max))

file.close()
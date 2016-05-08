from construct_train_data import get_label
from construct_train_data import gender_reg
from construct_train_data import age_reg
from construct_train_data import location_reg
from construct_train_data import profession_reg
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from utils import thread_load
from sklearn.cross_validation import train_test_split
import sys
import random
import time
from numpy import arange
import numpy
from sklearn.metrics import f1_score


total_data_arange={
        'zhihu_gender':arange(0.02,0.22,0.02),
        'zhihu_location':list(arange(0.02,0.1,0.02))+list(arange(0.1,0.7,0.1)),
        'zhihu_profession':list(arange(0.02,0.1,0.02))+list(arange(0.1,0.7,0.1)),
        'weibo_gender':list(arange(0.02,0.1,0.02))+list(arange(0.1,0.7,0.1)),
        'weibo_location':list(arange(0.02,0.1,0.02))+list(arange(0.1,0.7,0.1)),
        }
def get_simple_embedding(fname):
    return thread_load(fname)

def get_neibor_embedding(fname):
    data = thread_load(fname)
    embedding = dict()
    for uid, e in data.items():
        if len(e) < 2:
            continue
        # embedding[uid] = list(e[0]) + list(e[1]) + list(e[2]) + list(e[3]) + list(e[4]) + list(e[5])
        #embedding[uid] = list(e[0]) + list(e[1]) + list(e[2][-1]) + list(e[3][-1]) + list(e[4][-1]) + list(e[5][-1])
        embedding[uid] = list(e[0]) + list(e[1])
        #embedding[uid] = list(numpy.array(e[0]) + numpy.array(e[1]))
        # embedding[uid] = list(e[0]) + list(e[1]) + list(e[3]) + list(e[5])
        # embedding[uid]=e[0]+e[1]
    return embedding


def evaluate(labels, embedding):
    from collections import Counter
    uids = list(set(embedding.keys()) & set(labels.keys()))
    X = map(lambda uid: embedding[uid], uids)
    Y = map(lambda uid: labels[uid], uids)
    print('\t', dict(Counter(Y)))
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
        random_state=0
    )
    tuned_parameters = [
        {
            'kernel': ['rbf'],
            'gamma': [1e-2, 1e-3, 1e-4],
            'C': [1, 10, 100, 500, 1000]
        },
        {
            'kernel': ['linear'],
            'C': [1, 10, 100, 500, 1000]
        }
    ]
    print("# Tuning hyper-parameters for f1_weighted")
    print()

    clf = GridSearchCV(
        SVC(C=1),
        tuned_parameters,
        cv=5,
        scoring='f1_weighted',
        n_jobs=12
    )
    clf.fit(X_train, y_train)
    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in clf.grid_scores_:
        print(
            "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params)
        )
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred, digits=3))
    print()
    sys.stdout.flush()


def simple_evaluate(labels, embedding, params, count, data_range, uids):
    # simple_evaluate function uses default params without any params tuning
    from collections import Counter
    uids = list(set(uids) & set(embedding.keys()) & set(labels.keys()))
    #random.shuffle(uids)
    #uids = uids[0:count]
    #X = map(lambda uid: embedding[uid], uids)
    #Y = map(lambda uid: labels[uid], uids)
    #print('\t', dict(Counter(Y)))
    #sys.stdout.flush()
    #if params['kernel'] == 'linear':
    #    clf = SVC(C=params['C'], kernel=params['kernel'])
    #else:
    #    clf = SVC(
    #                C=params['C'],
    #                kernel=params['kernel'],
    #                gamma=params['gamma']
    #            )
    #clf=LogisticRegression()
    #clf = SVC()
    #test_X=X[-10000:]
    #test_Y=Y[-10000:]
    #print('\t', dict(Counter(test_Y)))
    #train_X=X[:-100000]
    #train_Y=Y[:-100000]
    #score_names = [
    #    'precision_weighted', 'recall_weighted', 'f1_weighted', 'f1_micro',
    #    'f1_macro', 'roc_auc'
    #]
    #for score_name in score_names:
    #    scores = cross_validation.cross_val_score(clf,
    #                                              X,
    #                                              Y,
    #                                              cv=2,
    #                                              scoring=score_name)
    #    print("%s:\t%0.3f (+/- %0.3f)" %
    #          (score_name, scores.mean(), scores.std() * 2))
    results=[]
    micro=[]
    macro=[]
    weighted=[]
    for data_count in data_range:
        random.shuffle(uids)
        X = map(lambda uid: embedding[uid], uids)
        Y = map(lambda uid: labels[uid], uids)
        results.append('Label ratio: %f'%data_count)
        data_count=int(data_count*len(uids))
        results.append('Label count: %d'%data_count)
        train_X=X[0:data_count]
        train_Y=Y[0:data_count]
        test_X=X[data_count:]
        test_Y=Y[data_count:]
        #clf=SVC()
        #clf=SVC(kernel='linear')
        clf=LogisticRegression()
        start_time=time.time()
        clf.fit(train_X,train_Y)
        predicted_Y=clf.predict(test_X)
        results.append('Time: %f'%(time.time()-start_time))
        results.append('Y: '+str(dict(Counter(Y))))
        results.append('Train Y: '+str(dict(Counter(train_Y))))
        results.append('Test Y: '+str(dict(Counter(test_Y))))
        results.append('Perdicted Y: '+str(dict(Counter(predicted_Y))))
        results.append(classification_report(test_Y, predicted_Y, digits=3))
        micro.append(f1_score(test_Y, predicted_Y, average='micro'))
        macro.append(f1_score(test_Y, predicted_Y, average='macro'))
        weighted.append(f1_score(test_Y, predicted_Y, average='weighted'))
        sys.stdout.flush()
    results.append('\t'.join(map(lambda x:str(x), micro)))
    results.append('\t'.join(map(lambda x:str(x), macro)))
    results.append('\t'.join(map(lambda x:str(x), weighted)))
    return results


def output_results(results,fname):
    f=open('./results/'+fname,'w')
    for r in results:
        f.write(str(r)+'\n')

def evaluate_baseline(fname, data_count, attibute=['profession']):
    deepwalk_params = [
        {'kernel': 'rbf',
         'C': 1000,
         'gamma': 0.001}, {'kernel': 'rbf',
                           'C': 100,
                           'gamma': 0.001}, {'kernel': 'rbf',
                                             'C': 10,
                                             'gamma': 0.001}
    ]
    line_params = [
        {'kernel': 'linear', 'C': 1},
        {'kernel': 'rbf', 'C': 100, 'gamma': 0.001},
        {'kernel': 'linear', 'C': 1000, 'gamma': 0.001}
    ]
    if 'deepwalk' in fname:
        print('======Deepwalk======')
        baseline='deepwalk'
        params = deepwalk_params
    if 'line' in fname:
        print('======LINE======')
        params = line_params
        baseline='line'
    if 'weibo' in fname:
        website = 'weibo'
    else:
        website = 'zhihu'
    embedding = get_simple_embedding(fname)
    uids=[line.strip() for line in open('./%s_intersect_uid.data'%website)]
    # evaluate(get_label(website, 1, gender_reg), embedding)
    # evaluate(get_label(website, 2, age_reg), embedding)
    # evaluate(get_label(website, 3, location_reg), embedding)
    if 'gender' in attibute:
        results=simple_evaluate(
        get_label(website, 1, gender_reg), embedding, params[0], data_count,
        data_range=total_data_arange['%s_gender'%(website)],
        uids=uids
        )
        output_results(results,'%s_%s_%s_result.out'%(website,'gender',baseline))
    if 'age' in attibute:
        results=simple_evaluate(
        get_label(website, 2, age_reg), embedding, params[1], data_count,
        data_range=list(arange(0.05,0.95,0.05)),
        uids=uids
        )
        output_results(results,'%s_%s_%s_result.out'%(website,'age',baseline))
    if 'location' in attibute:
        results=simple_evaluate(
        get_label(website, 3, location_reg), embedding, params[2], data_count,
        data_range=total_data_arange['%s_location'%(website)],
        uids=uids
        )
        output_results(results,'%s_%s_%s_result.out'%(website,'location',baseline))
    if 'profession' in attibute:
        results=simple_evaluate(
        get_label(website, 4, profession_reg), embedding, params[2], data_count,
        data_range=total_data_arange['%s_profession'%(website)],
        uids=uids
        )
        output_results(results,'%s_%s_%s_result.out'%(website,'profession',baseline))


def evaluate_our_method(website, iter_count, data_count, attibute=['profession']):
    params = [
        {'kernel': 'rbf',
         'C': 100,
         'gamma': 0.001}, {'kernel': 'rbf',
                           'C': 10,
                           'gamma': 0.001}, {'kernel': 'rbf',
                                             'C': 10,
                                             'gamma': 0.001}
    ]
    print('======Our; Iter Count: %d======' % iter_count)
    embedding = get_neibor_embedding(
        './embedding/%s_user_embedding_using_neibors_%d.data.json' %
        (website, iter_count)
    )
    uids=[line.strip() for line in open('./%s_intersect_uid.data'%website)]
    # evaluate(get_label(website, 1, gender_reg), embedding)
    # evaluate(get_label(website, 2, age_reg), embedding)
    # evaluate(get_label(website, 3, location_reg), embedding)
    if 'gender' in attibute:
        results=simple_evaluate(
        get_label(website, 1, gender_reg), embedding, params[0], data_count,
        data_range=total_data_arange['%s_gender'%(website)],
        uids=uids
        )
        output_results(results,'%s_%s_%s_result_%d.out'%(website,'gender','our',iter_count))
    if 'age' in attibute:
        results=simple_evaluate(
        get_label(website, 2, age_reg), embedding, params[1], data_count,
        data_range=list(arange(0.05,0.95,0.05)),
        uids=uids
        )
        output_results(results,'%s_%s_%s_result_%d.out'%(website,'age','our',iter_count))
    if 'location' in attibute:
        results=simple_evaluate(
        get_label(website, 3, location_reg), embedding, params[2], data_count,
        data_range=total_data_arange['%s_location'%(website)],
        uids=uids
        )
        output_results(results,'%s_%s_%s_result_%d.out'%(website,'location','our',iter_count))
    if 'profession' in attibute:
        results=simple_evaluate(
        get_label(website, 4, profession_reg), embedding, params[2], data_count,
        data_range=total_data_arange['%s_profession'%(website)],
        uids=uids
        )
        output_results(results,'%s_%s_%s_result_%d.out'%(website,'profession','our', iter_count))


if __name__ == '__main__':
    data_count = 15000000
    website='zhihu'
    if sys.argv[1] == 'deepwalk':
        evaluate_baseline(
            './embedding/%s_user_embedding_using_deepwalk.data.json'%website,
            data_count=data_count
        )
    if sys.argv[1] == 'line':
        evaluate_baseline(
            './embedding/%s_user_embedding_using_line.data.json'%website,
            data_count=data_count)
    if sys.argv[1] == 'our':
        evaluate_our_method(website, iter_count=25670, data_count=data_count)
    # evaluate_our_method('zhihu',iter_count=70)
    # evaluate_our_method('zhihu',iter_count=10)
    # evaluate_our_method('zhihu',iter_count=20)
    # evaluate_our_method('zhihu',iter_count=30)
    # evaluate_our_method('zhihu',iter_count=40)
    # evaluate_our_method('zhihu',iter_count=50)
    print('Done')

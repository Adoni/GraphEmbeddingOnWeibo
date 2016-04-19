from construct_train_data import get_label
from construct_train_data import gender_reg
from construct_train_data import age_reg
from construct_train_data import location_reg
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from utils import thread_load
from sklearn.cross_validation import train_test_split
import sys
import random


def get_simple_embedding(fname):
    return thread_load(fname)


def get_neibor_embedding(fname):
    data = thread_load(fname)
    embedding = dict()
    for uid, e in data.items():
        if len(e) < 6:
            continue
        # embedding[uid] = list(e[0]) + list(e[1]) + list(e[2]) + list(e[3]) + list(e[4]) + list(e[5])
        embedding[uid] = list(e[0]) + list(e[1]) + list(e[2][-1]) + list(e[3][
            -1]) + list(e[4][-1]) + list(e[5][-1])
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


def simple_evaluate(labels, embedding, params, count=10000000):
    import time
    # simple_evaluate function uses default params without any params tuning
    from collections import Counter
    uids = list(set(embedding.keys()) & set(labels.keys()))
    random.shuffle(uids)
    uids = uids[0:count]
    X = map(lambda uid: embedding[uid], uids)
    Y = map(lambda uid: labels[uid], uids)
    print('\t', dict(Counter(Y)))
    sys.stdout.flush()
    # clf=LogisticRegression()
    for data_count in [20000,40000,60000,80000,100000]:
        print(data_count)
        start_time=time.time()
        clf = LogisticRegression()
        tmp_X=X[0:data_count]
        tmp_Y=Y[0:data_count]
        clf.fit(tmp_X,tmp_Y)
        print(classification_report(tmp_Y, clf.predict(tmp_X), digits=3))
        print(time.time()-start_time)

    sys.stdout.flush()


def evaluate_baseline(fname, data_count):
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
        {'kernel': 'rbf', 'C': 1000, 'gamma': 0.001}
    ]
    if 'deepwalk' in fname:
        print('======Deepwalk======')
        params = deepwalk_params
    if 'line' in fname:
        print('======LINE======')
        params = line_params
    if 'weibo' in fname:
        website = 'weibo'
    else:
        website = 'zhihu'
    embedding = get_simple_embedding(fname)
    # evaluate(get_label(website, 1, gender_reg), embedding)
    # evaluate(get_label(website, 2, age_reg), embedding)
    # evaluate(get_label(website, 3, location_reg), embedding)
    simple_evaluate(
        get_label(website, 1, gender_reg), embedding, params[0], data_count)
    # simple_evaluate(get_label(website, 2, age_reg), embedding, params[1])
    # simple_evaluate(
    #     get_label(website, 3, location_reg), embedding, params[2], data_count)


def evaluate_our_method(website, iter_count, data_count):
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
    # evaluate(get_label(website, 1, gender_reg), embedding)
    # evaluate(get_label(website, 2, age_reg), embedding)
    # evaluate(get_label(website, 3, location_reg), embedding)
    simple_evaluate(
        get_label(website, 1, gender_reg), embedding, params[0], data_count)
    # simple_evaluate(get_label(website, 2, age_reg), embedding, params[1])
    simple_evaluate(
        get_label(website, 3, location_reg), embedding, params[2], data_count)


if __name__ == '__main__':
    evaluate_baseline(
            './embedding/weibo_user_embedding_using_deepwalk.data.json',
            data_count=data_count
    )
    # evaluate_our_method('zhihu',iter_count=70)
    # evaluate_our_method('zhihu',iter_count=10)
    # evaluate_our_method('zhihu',iter_count=20)
    # evaluate_our_method('zhihu',iter_count=30)
    # evaluate_our_method('zhihu',iter_count=40)
    # evaluate_our_method('zhihu',iter_count=50)
    print('Done')

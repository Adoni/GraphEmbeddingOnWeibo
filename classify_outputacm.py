from small_utils.vector_reader import read_vectors
from construct_train_data import outputacm_reg
from construct_train_data import get_label
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from utils import thread_load
from numpy import arange
import random
import time
import sys
import numpy
import json

def get_simple_embedding(fname):
    return thread_load(fname)

def get_neibor_embedding(fname):
    data = thread_load(fname)
    embedding = dict()
    for uid, e in data.items():
        if len(e) < 2:
            continue
        # embedding[uid] = list(e[0]) + list(e[1]) + list(e[2]) + list(e[3]) + list(e[4]) + list(e[5])
        #embedding[uid] = list(e[0])# + list(e[2][-1]) + list(e[3][
        #embedding[uid] = list(e[1])# + list(e[2][-1]) + list(e[3][
        #embedding[uid] = list(e[0]) + list(e[1]) + list(e[2][-1]) + list(e[3][
        #    -1]) + list(e[4][-1]) + list(e[5][-1])
        #embedding[uid] = numpy.array(e[0])+numpy.array(e[1])
        embedding[uid] = list(e[0]) + list(e[1])
        # embedding[uid] = list(e[0]) + list(e[1]) + list(e[3]) + list(e[5])
        # embedding[uid]=e[0]+e[1]
    return embedding

def simple_evaluate(labels, embedding, data_range, uid_file):
    '''
    simple_evaluate function uses default params without any params tuning
    '''
    from collections import Counter
    #uids = list(set(embedding.keys()) & set(labels.keys()))
    uids=[line.strip() for line in open(uid_file)]
    results=[]
    micro=[]
    macro=[]
    weighted=[]
    random.shuffle(uids)
    X = map(lambda uid: embedding[uid], uids)
    Y = map(lambda uid: labels[uid], uids)
    json.dump({'X':X,'Y':Y}, open('PCA_file.data','w'))
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
        #clf=GaussianNB()
        start_time=time.time()
        clf.fit(train_X,train_Y)
        predicted_Y=clf.predict(test_X)
        results.append('Time: %f'%(time.time()-start_time))
        results.append('Y: '+str(dict(Counter(Y))))
        results.append('Train Y: '+str(dict(Counter(train_Y))))
        results.append('Test Y: '+str(dict(Counter(test_Y))))
        results.append('Perdicted Y: '+str(dict(Counter(predicted_Y))))
        results.append(classification_report(test_Y, predicted_Y, digits=3))
        print(classification_report(train_Y, clf.predict(train_X), digits=3))
        micro.append(f1_score(test_Y, predicted_Y, average='micro'))
        macro.append(f1_score(test_Y, predicted_Y, average='macro'))
        weighted.append(f1_score(test_Y, predicted_Y, average='weighted'))
        sys.stdout.flush()
    results.append('\t'.join(map(lambda x:str(x), micro)))
    results.append('\t'.join(map(lambda x:str(x), macro)))
    results.append('\t'.join(map(lambda x:str(x), weighted)))
    return results

def pca_show(labels, embedding, uid_file):
    '''
    simple_evaluate function uses default params without any params tuning
    '''
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    from collections import Counter
    #uids = list(set(embedding.keys()) & set(labels.keys()))
    uids=[line.strip() for line in open(uid_file)]
    X = numpy.array(map(lambda uid: embedding[uid], uids))
    Y = numpy.array(map(lambda uid: labels[uid], uids))
    pca = PCA(n_components=2)
    X_r = pca.fit(X).transform(X)
    plt.figure()
    target_names=['AAAI','CIKM','ICML', 'KDD', 'NIPS', 'SIGIR', ' WWW']
    for c, i, target_name in zip("bgrcmyk", [0, 1, 2,3,4,5,6], target_names):
        plt.scatter(X_r[y == i, 0], X_r[y == i, 1], c=c, label=target_name)
    plt.legend()
    plt.title('PCA of IRIS dataset')
    plt.show()

def output_results(results,fname):
    f=open('./results/'+fname,'w')
    for r in results:
        f.write(str(r)+'\n')

def main():
    website='outputacm'
    method='line'
    count=100
    if method=='line':
        embedding=get_simple_embedding('./embedding/%s_user_embedding_using_line.data.json'%website)
    if method=='our':
        embedding=get_neibor_embedding('./embedding/%s_user_embedding_using_neibors_%d.data.json'%(website,count))
    print(len(embedding))
    results=simple_evaluate(
        get_label(website, 1, outputacm_reg), embedding,
        data_range=list(arange(0.1,1,0.1)),
        uid_file='./%s_intersect_uid.data'%website
    )
    output_results(results,'%s_%s_result_%d.out'%(website,method,count))
    pass

if __name__=='__main__':
    main()


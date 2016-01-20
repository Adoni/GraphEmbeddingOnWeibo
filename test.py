import time
from utils import thread_load
from traditional_classfify import get_simple_embedding
from traditional_classfify import get_neibor_embedding
from construct_train_data import *
import json
import numpy


def dump(labels, embedding, fname):
    uids = list(set(embedding.keys()) & set(labels.keys()))
    X = map(lambda uid: embedding[uid], uids)
    Y = map(lambda uid: labels[uid], uids)
    X = map(lambda x: map(lambda d: str(d), x), X)
    Y = map(lambda y: str(y), Y)
    fout = open(fname + '_X.data', 'w')
    fout.write('%d %d\n' % (len(X), len(X[0])))
    fout.write('\n'.join(map(lambda x: ' '.join(x), X)))
    fout = open(fname + '_Y.data', 'w')
    fout.write('%d\n' % len(Y))
    fout.write('\n'.join(Y))
    #numpy.savetxt(fname+'_X.data',X)
    #numpy.savetxt(fname+'_Y.data',Y,fmt='%d')


if __name__ == '__main__':
    iter_count = 20
    fname = './embedding/user_embedding_using_neibors_%d.data.json' % iter_count
    #embedding=get_simple_embedding(fname)
    embedding = get_neibor_embedding(fname)
    dump(
        get_label(1, gender_reg), embedding, './training_data/neibor_gender_%d'
        % iter_count
    )

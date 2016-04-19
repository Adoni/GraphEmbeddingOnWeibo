import time
from utils import thread_load
from traditional_classfify import get_simple_embedding
from traditional_classfify import get_neibor_embedding
from construct_train_data import *
import json
import numpy


def dump_for_cpp(labels, embedding, fname):
    uids = list(set(embedding.keys()) & set(labels.keys()))
    X = map(lambda uid: embedding[uid], uids)
    Y = map(lambda uid: labels[uid], uids)
    X = map(lambda x: map(lambda d: str(d), x), X)
    Y = map(lambda y: str(y), Y)
    print len(X)
    fout = open(fname + '_X.data', 'w')
    fout.write('%d %d\n' % (len(X), len(X[0])))
    fout.write('\n'.join(map(lambda x: ' '.join(x), X)))
    fout = open(fname + '_Y.data', 'w')
    fout.write('%d\n' % len(Y))
    fout.write('\n'.join(Y))
    #numpy.savetxt(fname+'_X.data',X)
    #numpy.savetxt(fname+'_Y.data',Y,fmt='%d')


def main():
    iter_count = 20
    fname = './embedding/user_embedding_using_neibors_%d.data.json' % iter_count
    #embedding=get_simple_embedding(fname)
    embedding = get_neibor_embedding(fname)
    dump_for_cpp(
        get_label(1, gender_reg), embedding,
        './training_data/neibor_gender_%d' % iter_count
    )
    dump_for_cpp(
        get_label(2, age_reg), embedding,
        './training_data/neibor_age_%d' % iter_count
    )
    dump_for_cpp(
        get_label(3, location_reg), embedding,
        './training_data/neibor_location_%d' % iter_count
    )


def count_uids():
    f = open('./graph_data/weights.data')
    uids = []
    while 1:
        line = f.readline()
        uids.append(line.strip())
        if line == '':
            break
        line = f.readline()
        line = f.readline()
    print len(uids) - len(set(uids))


if __name__ == '__main__':
    #count_uids()
    main()
    print 'Done'

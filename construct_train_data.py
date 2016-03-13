#coding:utf8
import json
from multiprocessing.dummy import Pool as ThreadPool
import numpy
import random


def get_location_labels():
    labels = dict()
    with open('./location.label') as f_l:
        for line in f_l:
            line = line.strip().split(' ')
            key = line[0]
            key = key.replace('省', '')
            key = key.replace('省', '')
            key = key.replace('市', '')
            key = key.replace('维吾尔族自治区', '')
            key = key.replace('回族自治区', '')
            key = key.replace('壮族自治区', '')
            key = key.replace('特别行政区', '')
            labels[key] = int(line[1])
    return labels


location_labels = get_location_labels()


def gender_reg(v):
    if v == '男' or v == 'm':
        return 0
    elif v == '女' or v == 'f':
        return 1
    else:
        return None


def age_reg(v, split_point=25):
    try:
        age = 2015 - int(v)
        if 5 <= age <= 100:
            if age <= split_point:
                return 0
            else:
                return 1
            return age
        else:
            return None
    except:
        return None


def location_reg(v):
    v = v.strip().split(' ')[0]
    try:
        return location_labels[v]
    except:
        return None


def get_label(label_index, label_reg):
    labels = dict()
    for line in open('./user_attributes.data'):
        line = line.strip().split('||')
        uid = line[0]
        label = label_reg(line[label_index])
        if label == None:
            continue
        labels[uid] = label
    #print len(labels)
    return labels


def thread_load(file_name):
    print 'loading from %s' % file_name
    with open(file_name) as data_file:
        data = json.load(data_file)
    print 'loading done'
    return data


def load(file_names):
    pool = ThreadPool(len(file_names))
    results = pool.map(thread_load, file_names)
    pool.close()
    pool.join()
    return tuple(results)


def get_user_embedding_on_simple_embedding(embedding_file, out_filename):
    uids = [
        line.strip().split(' ')[0]
        for line in open('./graph_data/cleaned_first_graph.data')
    ]
    embedding = thread_load(embedding_file)
    user_embedding = dict()
    for uid in uids:
        try:
            user_embedding[uid] = embedding[uid]
        except:
            continue
    with open(out_filename, 'w') as outfile:
        json.dump(user_embedding, outfile)


def get_weights():
    f=open('./graph_data/weights.data')
    weights=dict()
    while 1:
        uid=f.readline().strip()
        if uid=='':
            break
        neibors=f.readline().strip().split(' ')
        weight=map(lambda x:int(x), f.readline().strip().split(' '))
        weights[uid]=dict(zip(neibors,weight))
    return weights

def construct_friends_embedding_with_certain_count(friend_embeddings):
    counts=[user_embedding_using_neibors_50.data.j]
    counts=[5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 390]
    result=[]
    for count in counts:
        tmp_embedding=random.sample(friend_embeddings,count)
        result.append(list(numpy.mean(tmp_embedding, axis=0)))
    return result

def get_user_embedding_with_friends(iter_count):
    uids = [
        line.strip().split(' ')[0]
        for line in open('./graph_data/cleaned_first_graph.data')
    ]
    weights=get_weights()
    embedding_file = './embedding/neibor_embedding_1_%d.data.json' % iter_count
    re_embedding_file = './embedding/neibor_embedding_2_%d.data.json' % iter_count
    graph_file = './graph_data/cleaned_second_graph.data.small.json'
    re_graph_file = './graph_data/reversed_cleaned_second_graph.data.small.json'
    graph, re_graph, embedding, re_embedding = load(
        [graph_file, re_graph_file, embedding_file, re_embedding_file]
    )
    #graph,re_graph=load([graph_file,re_graph_file])
    user_embedding = dict()
    print 'Start'
    for index, uid in enumerate(uids):
        print index
        if uid not in graph:
            print 'H1', uid
            continue
        if uid not in re_graph:
            print 'H2', uid
            continue
        if uid not in embedding:
            print 'H3', uid
            continue
        if uid not in re_embedding:
            print 'H4', uid
            continue

        user_embedding[uid] = []

        #1. append user's embedding
        user_embedding[uid].append(embedding[uid])
        #2. append user's reversed embedding
        user_embedding[uid].append(re_embedding[uid])
        #3. append user's embedding from who he or her follows
        e1 = []
        e2 = []
        for friend in graph[uid]:
            try:
                e1.append(re_embedding[friend])
                e2.append(embedding[friend])
            except:
                continue
        #user_embedding[uid].append(list(numpy.mean(e1, axis=0)))
        user_embedding[uid].append(construct_friends_embedding_with_certain_count(e1))
        #user_embedding[uid].append(list(numpy.mean(e2, axis=0)))
        user_embedding[uid].append(construct_friends_embedding_with_certain_count(e2))
        #4. append user's embedding from who he or her follows
        e1 = []
        e2 = []
        for friend in re_graph[uid]:
            try:
                e1.append(embedding[friend])
                e2.append(re_embedding[friend])
            except:
                continue
        #user_embedding[uid].append(list(numpy.mean(e1, axis=0)))
        user_embedding[uid].append(construct_friends_embedding_with_certain_count(e1))
        #user_embedding[uid].append(list(numpy.mean(e2, axis=0)))
        user_embedding[uid].append(construct_friends_embedding_with_certain_count(e2))

    with open(
        './embedding/user_embedding_using_neibors_%d.data.json' % iter_count,
        'w'
    ) as outfile:
        json.dump(user_embedding, outfile)


def main():
    #get_label(3,location_reg)
    #get_user_embedding()
    #get_user_embedding_with_friends(10)
    #get_user_embedding_with_friends(15)
    get_user_embedding_with_friends(20)
    #get_user_embedding_with_friends(25)
    #get_user_embedding_with_friends(30)
    #get_user_embedding_with_friends(50)
    #get_user_embedding_on_simple_embedding('./embedding/deepwalk_embedding.data.json','./embedding/user_embedding_using_deepwalk.data.json')
    #get_user_embedding_on_simple_embedding('./embedding/line_embedding.data.json','./embedding/user_embedding_using_line.data.json')
    pass


if __name__ == '__main__':
    main()
    #get_weights()
    print 'Done'

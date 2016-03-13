#coding:utf8
import json
from small_utils.vector_reader import read_vectors
from multiprocessing import Process
import time


def dump_vector(in_file_name):
    #将embedding数据存储为json格式
    print 'Dump file %s' % in_file_name
    out_file_name = in_file_name + '.json'
    vector = read_vectors(in_file_name, as_dict=True, as_list=True)
    with open(out_file_name, 'w') as outfile:
        json.dump(vector, outfile)


def dump_small_graph(in_file_name):
    #small_graph中存储了first graph中所有的uid的所有朋友，这些朋友可能是first graph中的也可能是second graph中的
    #本函数将small graph读入成字典形式并存储为json格式
    print 'Dump file %s' % in_file_name
    t = time.time()
    graph = dict()
    uids = [
        line.strip().split(' ')[0]
        for line in open('./graph_data/cleaned_first_graph.data')
    ]
    with open(in_file_name) as fin:
        for line in fin:
            pos = line.find(' ')
            if pos == -1:
                continue
            uid = line[0:pos]
            if uid not in uids:
                continue
            line = line.strip().split(' ')
            graph[uid] = line[1:]
    out_file_name = in_file_name + '.small.json'
    with open(out_file_name, 'w') as outfile:
        json.dump(graph, outfile)
    print time.time() - t


def dump_graph(in_file_name):
    #本函数将graph读入成字典形式并存储为json格式
    print 'Dump file %s' % in_file_name
    t = time.time()
    graph = dict()
    with open(in_file_name) as fin:
        for line in fin:
            line = line.strip().split(' ')
            graph[line[0]] = line[1:]
    out_file_name = in_file_name + '.json'
    with open(out_file_name, 'w') as outfile:
        json.dump(graph, outfile)
    print time.time() - t


def dump(f, in_file_name):
    #多线程序列化,传入函数名和该函数的参数
    p = Process(target=f, args=[in_file_name, ])
    p.start()


if __name__ == '__main__':
    #dump_graph('./graph_data/cleaned_second_graph.data')
    #dump_vector('./embedding/line_embedding.data')
    #dump_vector('./embedding/deepwalk_embedding.data')
    #dump_vector('./embedding/neibor_embedding_1_20.data')
    #dump_vector('./embedding/neibor_embedding_2_20.data')
    #dump(dump_graph,'./graph_data/first_graph.data')
    #dump(dump_graph,'./graph_data/reversed_first_graph.data')
    #dump(dump_small_graph,'./graph_data/cleaned_second_graph.data')
    #dump(dump_small_graph,'./graph_data/reversed_cleaned_second_graph.data')
    #dump(dump_vector,'./embedding/deepwalk_embedding.data')
    #dump(dump_vector,'./embedding/line_embedding.data')
    #dump(dump_vector,'./embedding/neibor_embedding_1_20.data')
    #dump(dump_vector,'./embedding/neibor_embedding_2_20.data')
    #dump(dump_vector,'./embedding/neibor_embedding_1_10.data')
    #dump(dump_vector,'./embedding/neibor_embedding_2_10.data')
    #dump(dump_vector,'./embedding/neibor_embedding_1_15.data')
    #dump(dump_vector,'./embedding/neibor_embedding_2_15.data')
    #dump(dump_vector, './embedding/neibor_embedding_1_25.data')
    #dump(dump_vector, './embedding/neibor_embedding_2_25.data')
    dump(dump_vector, './embedding/neibor_embedding_1_30.data')
    dump(dump_vector, './embedding/neibor_embedding_2_30.data')
    #dump(dump_vector, './embedding/neibor_embedding_1_50.data')
    #dump(dump_vector, './embedding/neibor_embedding_2_50.data')
    print 'Done'

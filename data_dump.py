import json
from small_utils.vector_reader import read_vectors
from multiprocessing import Process
import time

def dump_vector(in_file_name):
    print 'Dump file %s'%in_file_name
    out_file_name=in_file_name+'.json'
    vector=read_vectors(in_file_name, as_dict=True, as_list=True)
    with open(out_file_name, 'w') as outfile:
        json.dump(vector, outfile)

def dump_small_graph(in_file_name):
    print 'Dump file %s'%in_file_name
    t=time.time()
    graph=dict()
    uids=[line.strip().split(' ')[0] for line in open ('./graph_data/cleaned_first_graph.data')]
    with open(in_file_name) as fin:
        for line in fin:
            pos=line.find(' ')
            if pos==-1:
                continue
            uid=line[0:pos]
            if uid not in uids:
                continue
            line=line.strip().split(' ')
            graph[uid]=line[1:]
    out_file_name=in_file_name+'.small.json'
    with open(out_file_name, 'w') as outfile:
        json.dump(graph, outfile)
    print time.time()-t

def dump_graph(in_file_name):
    print 'Dump file %s'%in_file_name
    t=time.time()
    graph=dict()
    with open(in_file_name) as fin:
        for line in fin:
            line=line.strip().split(' ')
            graph[line[0]]=line[1:]
    out_file_name=in_file_name+'.json'
    with open(out_file_name, 'w') as outfile:
        json.dump(graph, outfile)
    print time.time()-t

def dump_weight():
    uids=[line.strip().split(' ')[0] for line in open('./graph_data/cleaned_first_graph.data')]
    with open('./graph_data/cleaned_second_graph.data.dump.json') as data_file:
        graph=json.load(data_file)
    print len(graph.keys())
    weights=dict()
    for uid in uids:
        neibors=set(graph[uid])
        weight=dict()
        for n in neibors:
            try:
                w=len(set(graph[n])&neibors)
                if w>0:
                    weight[n]=w
            except Exception as e:
                continue
        weights[uid]=weight
    with open('./graph_data/weight.data.dump.json', 'w') as outfile:
        json.dump(weights, outfile)

def dump(f,in_file_name):
    p=Process(target=f,args=[in_file_name,])
    p.start()

if __name__=='__main__':
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
    dump(dump_vector,'./embedding/neibor_embedding_1_50.data')
    dump(dump_vector,'./embedding/neibor_embedding_2_50.data')
    print 'Done'

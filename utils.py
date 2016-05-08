import json
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


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


def cat_result(fname):
    print '=========='
    micro_f1=[]
    macro_f1=[]
    weighted_f1=[]
    ratio=[]
    count=[]
    for line in open(fname):
        if line.startswith('Label count: '):
            count.append(line[line.find(':')+2:-1])
            continue
        if line.startswith('Label ratio: '):
            ratio.append(line[line.find(':')+2:-1])
            continue
        if line.startswith('avg / total'):
            line=line.strip().replace('      ','\t').replace('     ','\t').replace('    ','\t')
            line=line.split('\t')
            weighted_f1.append(line[3])
            continue
        if line.startswith('          0'):
            line=line.strip().replace('      ','\t').replace('     ','\t').replace('    ','\t')
            line=line.split('\t')
            micro_f1.append(line[3])
            continue
        if line.startswith('          1'):
            line=line.strip().replace('      ','\t').replace('     ','\t').replace('    ','\t')
            line=line.split('\t')
            macro_f1.append(line[3])
            continue
    for i in range(len(micro_f1)):
        if(float(micro_f1[i])>float(macro_f1[i])):
            micro_f1[i],macro_f1[i]=macro_f1[i],micro_f1[i]
    print('\t'.join(ratio))
    print('\t'.join(count))
    print('\t'.join(micro_f1))
    print('\t'.join(macro_f1))
    print('\t'.join(weighted_f1))
    #for i in range(0,len(count)):
    #    print('%s\t%s\t%s\t%s\t%s\t'%(ratio[i],count[i],micro_f1[i],macro_f1[i],weighted_f1[i]))

def construct_intersec_uids(file_names, output_name):
    embedding=load(file_names)
    uids=set(embedding[0].keys())
    for e in embedding[1:]:
        uids=uids & set(e.keys())
    fout=open('./%s_intersect_uid.data'%output_name,'w')
    for uid in uids:
        fout.write(uid+'\n')

def zhihu_result():
    print '=====Zhihu Gender====='
    compare([
        './results/zhihu_gender_our_result_80.out',
        './results/zhihu_gender_our_result_25690.out',
        './results/zhihu_gender_line_result.out',
        './results/zhihu_gender_deepwalk_result.out',
        ])
    print '=====Zhihu Location====='
    compare([
        './results/zhihu_location_our_result_25690.out',
        './results/zhihu_location_line_result.out',
        './results/zhihu_location_deepwalk_result.out',
        ])
    print '=====Zhihu Profession====='
    compare([
        './results/zhihu_profession_our_result_70.out',
        './results/zhihu_profession_our_result_25670.out',
        './results/zhihu_profession_our_result_25690.out',
        './results/zhihu_profession_line_result.out',
        './results/zhihu_profession_deepwalk_result.out',
        ])


def weibo_result():
    print '=====Weibo Gender====='
    compare([
        './results/weibo_gender_our_result_20.out',
        './results/weibo_gender_line_result.out',
        './results/weibo_gender_deepwalk_result.out',
        ]
        )
    print '=====Weibo Location====='
    compare([
        './results/weibo_location_our_result_20.out',
        './results/weibo_location_line_result.out',
        './results/weibo_location_deepwalk_result.out',
        ])
    print '=====Done====='

def outputacm_result():
    print '=====Outputacm====='
    compare([
        './results/outputacm_our_result_250.out',
        './results/outputacm_line_result.out',
        ]
        )

def process_to_latex(f1,method):
    for i in range(0,len(f1[0])):
        max_f1=-1
        for j in range(len(f1)):
            if max_f1<f1[j][i]:
                max_f1=f1[j][i]
        for j in range(len(f1)):
            if max_f1==f1[j][i]:
                f1[j][i]='\\textbf{%0.2f}'%(f1[j][i]*100)
            else:
                f1[j][i]='%0.2f'%(f1[j][i]*100)
    for j in range(len(f1)):
        f1[j]=' & '.join(f1[j])
        print('& '+method[j]+' & '+f1[j]+'\\\\')

def compare(fnames):
    micro=[]
    macro=[]
    weighted=[]
    method=[]
    for fname in fnames:
        for m in ['deepwalk','line','our']:
            if m in fname:
                method.append(m)
        result=open(fname).readlines()
        micro.append(map(lambda x:float(x), result[-3].strip().split()))
        macro.append(map(lambda x:float(x), result[-2].strip().split()))
        weighted.append(map(lambda x:float(x), result[-1].strip().split()))
    print(method)
    print('Micro')
    process_to_latex(micro, method)
    print('Macro')
    process_to_latex(macro, method)
    print('Weighted')
    process_to_latex(weighted, method)
if __name__=='__main__':
    #construct_intersec_uids(
    #    [
    #        './embedding/outputacm_user_embedding_using_line.data.json',
    #        './embedding/outputacm_user_embedding_using_neibors_250.data.json'
    #        ],
    #    'outputacm'
    #)
    #construct_intersec_uids(
    #    [
    #        './embedding/dblp_user_embedding_using_line.data.json',
    #        './embedding/dblp_user_embedding_using_neibors_100.data.json'
    #        ],
    #    'dblp'
    #)
    #construct_intersec_uids(
    #    [
    #        './embedding/weibo_user_embedding_using_deepwalk.data.json',
    #        './embedding/weibo_user_embedding_using_line.data.json',
    #        './embedding/weibo_user_embedding_using_neibors_20.data.json'
    #        ],
    #    'weibo'
    #)
    #construct_intersec_uids(
    #    [
    #        './embedding/zhihu_user_embedding_using_deepwalk.data.json',
    #        './embedding/zhihu_user_embedding_using_line.data.json',
    #        './embedding/zhihu_user_embedding_using_neibors_20.data.json'
    #        ],
    #    'zhihu'
    #)
    #construct_intersec_uids(
    #    [
    #        './embedding/zhihu_user_embedding_using_deepwalk.data.json',
    #        './embedding/zhihu_user_embedding_using_line.data.json',
    #        './embedding/min5_zhihu_user_embedding_using_neibors_50.data.json'
    #        ],
    #    'zhihu'
    #)
    #weibo_result()
    zhihu_result()
    #outputacm_result()
    print('Done')

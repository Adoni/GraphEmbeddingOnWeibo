import time

def get_second_uids():
    uids=[]
    for line in open('./graph_data/cleaned_second_graph.data'):
        uids.append(line[0:line.find(' ')])
        print uids[-1]
        time.sleep(1)
    print 'get uids done'
    return set(uids)

def enlarge_dataset():
    uids=get_second_uids()
    f=open('./expended_user_profile','a')
    keywords=['gender', 'birthYear', 'location']
    for index in [1,2,3]:
        file_name='/users3/zyli/hbase_api/node04/weibo_sina_part%d'%index
        for line in open(file_name):
            uid=line[0:line.find('\t')]
            if uid not in uids:
                continue
            profile=[]
            for key in keywords:
                try:
                    l=line.find(key)
                    v=line[l:line.find('\t',l)]
                    if v=='':
                        v='None'
                    profile.append(v)
                except:
                    profile.append('None')
                    continue
            f.write(uid+'||'+'||'.join(profile)+'\n')

if __name__=='__main__':
    #enlarge_dataset()
    get_second_uids()
    print 'Done'

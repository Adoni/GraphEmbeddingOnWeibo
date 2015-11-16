from small_utils.progress_bar import progress_bar

def get_id_map():
    ids=[]
    for line in open('./id_map.txt'):
        ids.append(line.strip().split(' '))
    return dict(ids)

def map_uids():
    uids=[line.split('||')[0] for line in open('user_attributes.data')]
    id_map=get_id_map()
    new_uids=map(lambda uid:id_map[uid] if uid in id_map else 'None',uids)
    open('first_uids.data','w').write('\n'.join(list(new_uids)))
    return set(new_uids)

def get_first_uids():
    uids=[line.split('||')[0] for line in open('user_attributes.data')]
    return set(uids)

def get_second_uids():
    first_uids=get_first_uids()
    second_uids=[]
    for line in open('./first_graph.data'):
        second_uids+=line.strip().split()[2:]
    second_uids=set(second_uids)-first_uids
    return set(second_uids)

def remove_surrounding_nodes(fname):
    uids=[line.split(' ')[0] for line in open(fname)]
    uids=set(uids)
    fout=open('cleaned_'+fname,'w')
    bar=progress_bar(len(uids))
    for index,line in enumerate(open(fname)):
        bar.draw(index+1)
        line=line.strip().split(' ')
        line=filter(lambda uid:uid in uids,line)
        fout.write(' '.join(line)+'\n')

def construct_graph(fname,uids):
    print '==========='
    print fname
    print len(uids)
    bar=progress_bar(len(uids))
    fout=open(fname,'w')
    index=0
    for line in open('./remap_weibo_graph.data'):
        uid=line[0:line.find(' ')]
        if uid in uids:
            fout.write(line)
            index+=1
            bar.draw(index)

def main():
    uids=get_first_uids()
    fname='first_graph.data'
    construct_graph(fname,uids)
    uids=get_second_uids()
    fname='second_graph.data'
    construct_graph(fname,uids)

if __name__=='__main__':
    #get_first_uids()
    #main()
    remove_surrounding_nodes('first_graph.data')
    print 'Done'

def statistics_graph(graph_name):
    degree=0
    node=0
    for line in open(graph_name):
        degree+=len(line.split(' '))
        node+=1
    print('%s\t%d\t%d\t%0.3f'%(graph_name,degree,node,1.0*degree/node))

if __name__=='__main__':
    statistics_graph('./outputacm_graph.data')
    statistics_graph('./cleaned_weibo_graph.data')
    statistics_graph('./cleaned_zhihu_graph.data')
    statistics_graph('./dblp_graph.data')

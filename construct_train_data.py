#coding:utf8

def get_location_labels():
    labels=dict()
    with open('./location.label') as f_l:
        for line in f_l:
            line=line.strip().split(' ')
            labels[line[0]]=int(line[1])
    return labels

location_labels=get_location_labels()

def gender_reg(v):
    if v=='男' or v=='m':
        return 0
    elif v=='女' or v=='f':
        return 1
    else:
        return None

def age_reg(v,split_point=25):
    try:
        age=2015-int(v)
        if 5<=age<=100:
            if age<=split_point:
                return 0
            else:
                return 1
            return age
        else:
            return None
    except:
        return None

def location_reg(v):
    v=v.strip().split(' ')[0]
    try:
        return location_labels[v]
    except:
        return None

def get_label(label_index,label_reg):
    labels=dict()
    for line in open('./user_attributes.data'):
        line=line.strip().split('||')
        uid=line[0]
        label=label_reg(line[label_index])
        if label==None:
            continue
        labels[uid]=label
    print len(labels)
    return labels

def main():
    get_label(3,location_reg)

if __name__=='__main__':
    main()

from collections import Counter
def counter_location():
    locations=[]
    for line in open('./user_attributes.data'):
        line=line.strip().split('||')[-1].split(' ')[0]
        if line=='None':
            continue
        locations.append(line)
    locations=Counter(locations)
    for i in locations:
        print i,'\t',locations[i]

if __name__=='__main__':
    counter_location()

import random
import sys
import rtree
import json

def gen_pfc(pfc_cnt,edge_cnt,edges):
    info = []
    for i in range(0,pfc_cnt):
        edge_id = random.randint(0,edge_cnt)
        edge_dist = search_edge(edges,edge_id)['DISTANCE']
        location = random.uniform(0,edge_dist)
        inf = {'EDGE_ID':edge_id,'NODE_ID':i,'LOC':location}
        info.append(inf)
    return info

def search_edge(edges,edge_id):
    for edge in edges:
        if edge['EDGE_ID'] == edge_id:
            return edge
     
def file_write(pfcs,filename):
    f = open(filename,"w")
    for pfc in pfcs:
        f.write(json.dumps(pfc))
        f.write('\n')
        f.flush()
    f.close()

def load(filename):
    f = open(filename,'r')
    list_data = []
    for line in f:
        data = json.loads(line)
        list_data.append(data)
    return list_data

def gen_rtree(vertex):
    idx = rtree.index.Index()
    cnt = 0
    for v in vertex:
        idx.insert(cnt,(v['LON'],v['LAT'],v['LON'],v['LAT']))
        cnt = cnt + 1
    return idx

#------------------------------------------------------------------------------------------------#

vertex = load(sys.argv[1])
tree = gen_rtree(vertex)

edges = load(sys.argv[2])
len_e = len(edges) 

potential = gen_pfc(int(sys.argv[3]),len_e,edges)
facility = gen_pfc(int(sys.argv[4]),len_e,edges)
client = gen_pfc(int(sys.argv[5]),len_e,edges)
list_pfc = [potential,facility,client]
list_pfc_str = ['potential','facility','client']
for idx,pfc in enumerate(list_pfc):
    file_write(pfc,list_pfc_str[idx]+'.json')
    name = list_pfc_str[idx]+'_id'
    for i in pfc:
        for e in edges:
            if e['EDGE_ID'] == i['EDGE_ID']:
                if name in e:
                    e[name].append(i['NODE_ID'])
                else:
                    e[name] = [i['NODE_ID']]
        
file_write(edges,'refined_edge.json')




'''
.............................
할일:
    1. arg1=v, arg2=e
    2. vertex r tree
    3. potential projection
.............................

'''

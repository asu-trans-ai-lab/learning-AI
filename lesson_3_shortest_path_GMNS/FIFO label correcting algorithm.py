# _*_coding:utf-8 _*_
# @Time　　:2020/3/1/10:47
# @Author　 : Dr.Prase
#@ File　　  :modified label correcting algorithm.py
#@Software  :PyCharm
"""import basic packages"""
import pandas as pd
import numpy as np
import copy
g_node_list=[] #set of nodes
g_node_zone={} #set of node types
g_link_list=[] #set of arcs
g_adjacent_arc_list={} #set of arcs emanating from that node
g_shortest_path=[] #set of shortest paths
g_node_status=[] #set of node status
g_number_of_nodes=0 #number of nodes
g_origin=None   #source node
node_predecessor=[] #set of predecessor nodes
node_label_cost=[] #set of distance labels
SE_LIST=[] #scan eligible list
Max_label_cost=99999 #initialize distance label
"""import network data file and initialize corresponding variables"""
#read network node data
df_node=pd.read_csv('node.csv')
df_node=df_node.iloc[:,:].values
for i in range(len(df_node)):
    g_node_list.append(df_node[i,0])
    g_node_zone[df_node[i, 0]] = df_node[i, -1]
    g_number_of_nodes+=1
    g_adjacent_arc_list[df_node[i,0]]=[]
    if df_node[i, 3] == 1:
        g_origin = df_node[i, 0]
g_node_status=[0 for i in range(g_number_of_nodes)]#initialize node status
Distance=np.ones((g_number_of_nodes,g_number_of_nodes))*Max_label_cost #distance matrix
node_predecessor=[-1]*g_number_of_nodes
node_label_cost=[Max_label_cost]*g_number_of_nodes
node_predecessor[g_origin-1]=0
node_label_cost[g_origin-1] = 0
#read data of arcs
df_link=pd.read_csv('road_link.csv')
df_link=df_link.iloc[:,:].values
for i in range(len(df_link)):
    g_link_list.append((df_link[i,1],df_link[i,2]))
    Distance[df_link[i,1]-1,df_link[i,2]-1]=df_link[i,3]
    g_adjacent_arc_list[df_link[i,1]].append(df_link[i,2])
SE_LIST=[g_origin]
g_node_status[g_origin-1]=1
"""finding shortest path: scan arcs and check their optimality conditions"""
while len(SE_LIST):
    head=SE_LIST[0]#remove first node from scan eligible list
    SE_LIST.pop(0)
    g_node_status[head-1]=0
    adjacent_arc_list=g_adjacent_arc_list[head]#get arcs emanating from that node
    for tail in adjacent_arc_list:
        if node_label_cost[tail-1]>node_label_cost[head-1]+Distance[head-1,tail-1]:
            node_label_cost[tail-1]=node_label_cost[head-1]+Distance[head-1,tail-1]
            node_predecessor[tail-1]=head
            if g_node_status[tail-1]==0:
                SE_LIST.append(tail)
                g_node_status[tail-1]=1
"""generate shortest paths according to predecessor nodes"""
agent_id=1
o_zone_id=g_node_zone[g_origin]
for destination in g_node_list:
    if g_origin!=destination:
        d_zone_id=g_node_zone[destination]
        if node_label_cost[destination-1]==Max_label_cost:
            path = " "
            g_shortest_path.append([agent_id,o_zone_id,d_zone_id, path, node_label_cost[destination - 1]])
        else:
            to_node=copy.copy(destination)
            path = "%s" % to_node
            while node_predecessor[to_node-1]!=g_origin:
                path = "%s;" % node_predecessor[to_node - 1] + path
                g=node_predecessor[to_node-1]
                to_node=g
            path="%s;"%g_origin+path
            g_shortest_path.append([agent_id,o_zone_id,d_zone_id, path, node_label_cost[destination - 1]])
            print('from {} to {} the path is {}，length is {}'
                      .format(g_origin,destination,path,node_label_cost[destination-1]))
        agent_id+=1
"""put result into csv file"""
#transfer data into DataFrame
g_shortest_path=np.array(g_shortest_path)
col=['agent_id','o_zone_id','d_zone_id','node_sequence','distance']
file_data = pd.DataFrame(g_shortest_path, index=range(len(g_shortest_path)),columns=col)
file_data.to_csv('agent.csv',index=False)

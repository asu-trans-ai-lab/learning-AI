# _*_coding:utf-8 _*_
# @Time　　:2020/2/29/21:32
# @Author　 : Simon Xuesong Zhou at ASU xzhou74@asu.edu 
#@ File　　  :generic label correcting algorithm.py
#@Software  :PyCharm
"""import package"""
import pandas as pd
import numpy as np
import copy
"""define global variables"""
g_node_list=[] #set of node
g_node_zone={} #set of node type
g_link_list=[] #set of arc
g_shortest_path=[] #set of shortest path
g_origin=None   #source node of network
g_number_of_nodes=0#node number
node_predecessor=[]#set of predecessor node
node_label_cost=[]#set of distance label
Max_label_cost=99999#initial distance label
"""import network data file and initialize corresponding variables"""
#read data of nodes
df_node=pd.read_csv('node.csv')
df_node=df_node.iloc[:,:].values
for i in range(len(df_node)):
    g_node_list.append(df_node[i,0])
    g_node_zone[df_node[i,0]]=df_node[i,-1]
    g_number_of_nodes+=1
    if df_node[i,3]==1:
        g_origin=df_node[i,0]
Distance=np.ones((g_number_of_nodes,g_number_of_nodes))*Max_label_cost #distance matrix
node_predecessor=[-1]*g_number_of_nodes
node_label_cost=[Max_label_cost]*g_number_of_nodes
node_predecessor[g_origin-1]=0
node_label_cost[g_origin-1] = 0
#read data of arcs
df_link=pd.read_csv('link.csv')
df_link=df_link.iloc[:,:].values
for i in range(len(df_link)):
    g_link_list.append((df_link[i,1],df_link[i,2]))
    Distance[df_link[i,1]-1,df_link[i,2]-1]=df_link[i,3]
"""finding optimal solution: scan arc and check its optimality condition"""
while True:
    v=0 #number of arcs violating the optimality conditons
    for head,tail in g_link_list:
        if node_label_cost[tail-1]>node_label_cost[head-1]+Distance[head-1,tail-1]:
            node_label_cost[tail-1]=node_label_cost[head-1]+Distance[head-1,tail-1]
            node_predecessor[tail-1]=head
            v=v+1
    if v==0:
        break
"""generate shortest paths according to the predecessor node"""
agent_id=1
o_zone_id=g_node_zone[g_origin]
for destination in g_node_list:
    if g_origin!=destination:
        d_zone_id=g_node_zone[destination]
        if node_label_cost[destination-1]==Max_label_cost:
            path=" "
            g_shortest_path.append([agent_id,o_zone_id,d_zone_id,path,node_label_cost[destination-1]])
        else:
            to_node=copy.copy(destination)
            path="%s"%to_node
            while node_predecessor[to_node-1]!=g_origin:
                path="%s;"%node_predecessor[to_node-1]+path
                g=node_predecessor[to_node-1]
                to_node=g
            path="%s;"%g_origin+path
            g_shortest_path.append([agent_id,o_zone_id,d_zone_id, path, node_label_cost[destination - 1]])
            print('from {} to {} the path is {}，length is {}'
                      .format(g_origin,destination,path,node_label_cost[destination-1]))
        agent_id+=1
"""output result into csv file"""
#transform data into DataFrame
g_shortest_path=np.array(g_shortest_path)
col=['agent_id','o_zone_id','d_zone_id','node_sequence','distance']
file_data = pd.DataFrame(g_shortest_path, index=range(len(g_shortest_path)),columns=col)
file_data.to_csv('agent.csv',index=False)
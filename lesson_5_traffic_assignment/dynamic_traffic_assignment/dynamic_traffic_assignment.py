 # -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 15:32:44 2019

@author: Administrator
"""

import csv 
import numpy as np
import datetime
from collections import deque
from random import randint

# In[0] Initialization
g_number_of_nodes=0
g_node_list=[]
g_link_list=[]
g_agent_list=[]
g_node_seq_no_dict={}
g_seq_no_node_dict={}
g_agent_seq_no_dict={}

g_number_of_seconds_per_interval=60
g_Simulation_StartTimeInMin=99999
g_total_assignment_itration=10
g_Simulation_EndTimeInMin=0
g_start_sim_interval_no=0
max_label_cost=float('inf')
g_number_of_optimization_time_intervals=int((g_Simulation_EndTimeInMin-g_Simulation_StartTimeInMin)*60/g_number_of_seconds_per_interval)
g_end_sim_interval_no=g_start_sim_interval_no+g_number_of_optimization_time_intervals
g_safe_headway=1.4

g_number_of_nodes=0
g_number_of_links=0
g_number_of_agents=0

# In[1] construct properties for node, link network and agent
class Node():
    
    def __init__(self,name,node_id,control_type,control_type_name,
                 cycle_length_in_second,x,y,geometry):
        self.name=name
        self.node_id=node_id
        self.control_type=control_type
        self.control_type_name=control_type_name
        self.cycle_length_in_second=cycle_length_in_second
        self.x=x
        self.y=y
        self.geometry=geometry
        self.node_seq_no=0
        self.m_outgoing_link_list=[]
        self.m_incoming_link_list=[]
        self.initialization()
        
    def initialization(self):
        global g_number_of_nodes

        g_node_seq_no_dict[self.node_id]=g_number_of_nodes
        g_seq_no_node_dict[g_number_of_nodes]=self.node_id
        self.node_seq_no=g_number_of_nodes
        
        g_number_of_nodes+=1
        
        if g_number_of_nodes%1000==0:
            print('reading',g_number_of_nodes,'nodes')
        
   
class Link():
    
    def __init__(self,name,link_id,from_node_id,to_node_id,direction,length,
                 number_of_lanes,speed_limit,lane_cap,link_type,link_type_name,
                 jam_density,wave_speed,demand_type_code,count_sensor_id,
                 speed_sensor_id,geometry):
        self.name=name
        self.link_id=link_id
        self.from_node_id=from_node_id
        self.to_node_id=to_node_id
        self.direction=direction
        self.length=float(length)
        self.number_of_lanes=int(number_of_lanes)
        self.speed_limit=int(speed_limit)
        self.lane_cap=float(lane_cap)
        self.link_capacity=self.number_of_lanes*self.lane_cap
        self.link_type=link_type
        self.link_type_name=link_type_name
        self.jam_density=jam_density
        self.wave_speed=wave_speed
        self.demand_type_code=demand_type_code
        self.count_sensor_id=count_sensor_id
        self.speed_sensor_id=speed_sensor_id
        self.geometry=geometry
        self.link_seq_no=0
        self.free_flow_travel_time_in_min=self.length/self.speed_limit*60
        self.free_flow_travel_time_in_sim_interval=self.free_flow_travel_time_in_min*60/g_number_of_seconds_per_interval
        self.flow_volume=[0 for i in range(g_number_of_optimization_time_intervals)]
        self.travel_time=[self.free_flow_travel_time_in_min for i in range(g_number_of_optimization_time_intervals)]
        self.travel_time_in_simu_interval=[round(self.free_flow_travel_time_in_sim_interval) for i in range(g_number_of_optimization_time_intervals)]
        self.BPR_alpha=0.15
        self.BPR_beta=4.0
        self.initialization()
    
    def time_dependent_link_travel_time_BPR(self):
        
        for i in range(g_number_of_optimization_time_intervals):
            self.travel_time[i]=self.free_flow_travel_time_in_min*(1+self.BPR_alpha*pow(self.flow_volume[i]/max(0.0001,self.link_capacity),self.BPR_beta))
            self.travel_time_in_simu_interval[i]=round(self.travel_time[i]*60/g_number_of_seconds_per_interval)
      
   
    def initialization(self):
        global g_number_of_links
        
        self.from_node_seq_no=g_node_seq_no_dict[self.from_node_id]
        self.to_node_seq_no=g_node_seq_no_dict[self.to_node_id]
        
        self.link_seq_no=g_number_of_links
        g_number_of_links+=1
        
        g_node_list[self.from_node_seq_no].m_outgoing_link_list.append(self)
        g_node_list[self.to_node_seq_no].m_incoming_link_list.append(self)
        
        if g_number_of_links%1000==1:
            print('reading',g_number_of_links,'links')
            
    def allocate_memory(self):
        self.m_link_outflow_capacity=np.ones(g_number_of_optimization_time_intervals)*self.link_capacity
        self.m_link_cumulative_arrival=np.ones(g_number_of_optimization_time_intervals)
        self.m_link_cumulative_departure=np.ones(g_number_of_optimization_time_intervals)
        self.m_link_volume=np.ones(g_number_of_optimization_time_intervals)
        self.m_link_travel_time=np.ones(g_number_of_optimization_time_intervals)
 
class Agent():
    
    def __init__(self,agent_id,from_origin_node_id,to_destination_node_id,
                 departure_time_in_min,arrival_time_in_min,complete_flag,
                 travel_time_in_min,distance,path_node_sequence,path_time_sequence):
        self.agent_id=agent_id
        self.from_origin_node_id=from_origin_node_id
        self.from_origin_node_seq_no=g_node_seq_no_dict[self.from_origin_node_id]
        self.to_destination_node_id=to_destination_node_id
        self.to_destination_node_seq_no=g_node_seq_no_dict[self.to_destination_node_id]
        self.departure_time_in_min=float(departure_time_in_min)
        self.arrival_time_in_min=float(arrival_time_in_min)
        self.complete_flag=complete_flag
        self.travel_time_in_min=travel_time_in_min
        self.distance=distance
        self.path_node_sequence=path_node_sequence
        self.path_time_sequence=path_time_sequence
        self.departure_time_in_simu_interval=round(self.departure_time_in_min*60/g_number_of_seconds_per_interval)
        self.path_cost=0
        self.PCE_factor=1
        self.arrive_time_in_min_in_assignment=0
        self.arrive_time_in_simu_interval=0
        self.travel_time_in_min_in_assignment=0
        self.path_node_seq_no=''
        self.agent_path_link_seq_no_list=[]
        self.agent_path_node_seq_no_list=[]
        self.agent_path_node_seq_list=[]
        self.initialization()
        
    def initialization(self):
        global g_number_of_agents
        global g_Simulation_StartTimeInMin
        global g_Simulation_EndTimeInMin       
        
        if (self.from_origin_node_id not in g_node_seq_no_dict.keys()) or (self.to_destination_node_id not in g_node_seq_no_dict.keys()):
            print('agent'+self.agent_id+'origin or destination node dose not exist in node set, please check!')
            
        else:
            g_agent_seq_no_dict[self.agent_id]=g_number_of_agents
            g_number_of_agents+=1
            
                        
            if self.departure_time_in_min<g_Simulation_StartTimeInMin:
                g_Simulation_StartTimeInMin=self.departure_time_in_min
            if self.departure_time_in_min>g_Simulation_EndTimeInMin:
                g_Simulation_EndTimeInMin=self.departure_time_in_min
            
            
            if g_number_of_agents%10000==0:
                print('reading'+str(g_number_of_agents)+'agents')
       
    def allocate_memory(self):
        self.m_agent_path_link_seq_no_size=len(self.agent_path_link_seq_no_list)
        
        if self.m_agent_path_link_seq_no_size>0:
            self.m_Veh_LinkArrivalTime_in_sim_interval=np.ones(self.m_agent_path_link_seq_no_size)
            self.m_Veh_LinkDepartureTime_in_sim_interval=np.ones(self.m_agent_path_link_seq_no_size)
            
            first_link_no=self.agent_path_link_seq_no_list[0]
            self.m_Veh_LinkArrivalTime_in_sim_interval[0]=self.departure_time_in_simu_interval
            self.m_Veh_LinkDepartureTime_in_sim_interval[0]=self.m_Veh_LinkArrivalTime_in_sim_interval[0]+g_link_list[first_link_no].free_flow_travel_time_in_sim_interval
            
            relative_simualtion_interval_departure_time=RelativeSimulationInterval(self.departure_time_in_simu_interval)
            g_link_list[first_link_no].m_LinkCumulativeArrival[relative_simualtion_interval_departure_time]+=1
            
    def FieldCaculation(self):
        self.travel_time_in_min_in_assignment=self.arrive_time_in_min_in_assignment-self.departure_time_in_min
        self.path_node_seq_no=TransforAgentPath(self.agent_path_node_seq_list)
        self.number_of_nodes=len(self.agent_path_node_seq_no_list)
        
     
 
# In[1] input data
def read_input_data():
    global g_node_list
    global g_link_list
    global g_agent_list
    global g_Simulation_StartTimeInMin
    global g_Simulation_EndTimeInMin
    global g_number_of_optimization_time_intervals
    global g_start_sim_interval_no
    global g_end_sim_interval_no
    
    with open('input_node.csv') as node:
        input_node = csv.reader(node)
        next(input_node)
        g_node_list=[Node(*row) for row in input_node]
        
    with open('input_agent.csv') as agent:
        input_agent = csv.reader(agent)
        next(input_agent)
        g_agent_list=[Agent(*row) for row in input_agent]
        
    number_of_optimization_time_intervals=int((g_Simulation_EndTimeInMin+60-g_Simulation_StartTimeInMin)*60/g_number_of_seconds_per_interval)
        
    g_number_of_optimization_time_intervals=max(1,number_of_optimization_time_intervals)

       
    with open('input_link.csv') as link:
        input_link = csv.reader(link)
        next(input_link)
        g_link_list=[Link(*row) for row in input_link]        
 

        
         
    print('g_Simulation_StartTimeInMin'+str(g_Simulation_StartTimeInMin))
    print('g_Simulation_EndTimeInMin'+str(g_Simulation_EndTimeInMin))
        
    
    print('g_number_of_optimization_time_intervals'+str(g_number_of_optimization_time_intervals))
    
    g_start_sim_interval_no=g_Simulation_StartTimeInMin*60/g_number_of_seconds_per_interval
    g_end_sim_interval_no=g_Simulation_EndTimeInMin*60/g_number_of_seconds_per_interval
    
 
# In[1] caculate shortest path for any od pairs at any time    
class Network():
    
    def allocate_memory(self):
        self.node_predecessor=np.ones(g_number_of_nodes,dtype=int)*-1
        self.node_label_cost=np.ones(g_number_of_nodes,dtype=int)*max_label_cost
        self.link_predecessor=np.ones(g_number_of_nodes,dtype=int)*-1
    
    def time_dependent_label_correcting(self,origin_node,destination_node,departure_time_in_min,departure_time_in_simu_interval):
        if len(g_node_list[origin_node].m_outgoing_link_list)==0:
            return 0
        self.allocate_memory()
        self.node_label_cost[origin_node]=departure_time_in_simu_interval
        self.departure_time_in_simu_interval_relative=RelativeSimulationInterval(departure_time_in_simu_interval)
        current_node_cost_relative=self.departure_time_in_simu_interval_relative
        SEList=deque()
        SEList_all=[]
        SEList.append(origin_node)
        SEList_all.append(origin_node)
    
        while len(SEList)>0:
            from_node=SEList[0]
            current_node_cost=self.node_label_cost[from_node]
            current_node_cost_relative=RelativeSimulationInterval(current_node_cost)
            
            SEList.popleft()
            for outging_link in g_node_list[from_node].m_outgoing_link_list:
                to_node=outging_link.to_node_seq_no

                new_to_node_cost=self.node_label_cost[from_node]+outging_link.travel_time[current_node_cost_relative]
                if new_to_node_cost<self.node_label_cost[to_node]:
                    
                    self.node_label_cost[to_node]=new_to_node_cost
                    self.node_predecessor[to_node]=from_node
                    self.link_predecessor[to_node]=outging_link.link_seq_no
                    
                    if to_node in SEList_all:
                        SEList.insert(0,to_node)
                        
                    else:
                        SEList.append(to_node)
                                                
                    SEList_all.append(to_node)
                    
        if destination_node>=0 and self.node_label_cost[destination_node]<max_label_cost:
            return 1
        else:
            return -1
                    
    def find_path_for_agents(self,iteration_no):
        for i in range(len(g_agent_list)):
            residual=i%(iteration_no+1)
            if residual==0:
                g_agent_list[i].agent_path_link_seq_no_list=[]
                g_agent_list[i].agent_path_node_seq_no_list=[]
                g_agent_list[i].agent_path_node_seq_list=[]
                
                return_value=self.time_dependent_label_correcting(g_agent_list[i].from_origin_node_seq_no,g_agent_list[i].to_destination_node_seq_no,g_agent_list[i].departure_time_in_min,
                                                                  g_agent_list[i].departure_time_in_simu_interval)
                
                if return_value==-1:
                    print('agent '+i+'can not find shorstest path and network has negative cycle')
                    continue
                
                current_node_seq_no=g_agent_list[i].to_destination_node_seq_no
                g_agent_list[i].path_cost=self.node_label_cost[current_node_seq_no]
                g_agent_list[i].arrive_time_in_min_in_assignment=self.node_label_cost[current_node_seq_no]
                
                while current_node_seq_no>=0:
                    current_link_seq_no=self.link_predecessor[current_node_seq_no]
                    
                    if current_link_seq_no>=0:
                        g_agent_list[i].agent_path_link_seq_no_list.append(current_link_seq_no)
                        
                    g_agent_list[i].agent_path_node_seq_no_list.append(current_node_seq_no)
                    g_agent_list[i].agent_path_node_seq_list.append(int(g_seq_no_node_dict[current_node_seq_no]))
                    current_node_seq_no=self.node_predecessor[current_node_seq_no]
                
                g_agent_list[i].agent_path_link_seq_no_list.reverse()
                g_agent_list[i].agent_path_node_seq_no_list.reverse()
                
            number_of_links_in_path=len(g_agent_list[i].agent_path_link_seq_no_list)
                
            arrive_timestamp_link=int(g_agent_list[i].departure_time_in_simu_interval)
            arrive_timestamp_link_relative=RelativeSimulationInterval(arrive_timestamp_link)

           
            for j in range(number_of_links_in_path):

                current_link_travel_time_in_simu_interval=g_link_list[g_agent_list[i].agent_path_link_seq_no_list[j]].travel_time_in_simu_interval[arrive_timestamp_link_relative]
                departure_timestamp_link_relative=arrive_timestamp_link_relative+current_link_travel_time_in_simu_interval
                
                if departure_timestamp_link_relative>=g_number_of_optimization_time_intervals:
                    for t in range(arrive_timestamp_link_relative,departure_timestamp_link_relative):
                        g_link_list[g_agent_list[i].agent_path_link_seq_no_list[j]].flow_volume[t]+=g_agent_list[i].PCE_factor
                        g_link_list[g_agent_list[i].agent_path_link_seq_no_list[j]].time_dependent_link_travel_time_BPR()
                else:
                    for t in range(arrive_timestamp_link_relative,departure_timestamp_link_relative):
                        g_link_list[g_agent_list[i].agent_path_link_seq_no_list[j]].flow_volume[t]+=g_agent_list[i].PCE_factor
                        g_link_list[g_agent_list[i].agent_path_link_seq_no_list[j]].time_dependent_link_travel_time_BPR()
         
                arrive_timestamp_link_relative=departure_timestamp_link_relative
                
# In[1] caculate shortest path for any od pairs at any time  
def TransforAgentPath(original_list):
    original_list.reverse()
    
    return str(original_list).replace(',',';')[1:-1]
    
    
def RelativeSimulationInterval(time_in_simu_interval):
    relative_simulation_interval=int(time_in_simu_interval-g_start_sim_interval_no)
    return relative_simulation_interval

def TrafficAssignment():
    network=Network()
    
    for i in range(g_total_assignment_itration):
        print('iteration number is '+str(i))
        
      
        for l in range(g_number_of_links):
            current_flow_volume=g_link_list[l].flow_volume[g_number_of_optimization_time_intervals-1]
            g_link_list[l].time_dependent_link_travel_time_BPR()
           
            g_link_list[l].flow_volume=[0 for i in range(g_number_of_optimization_time_intervals)]
         
        network.find_path_for_agents(i)
        
# In[1] caculate shortest path for any od pairs at any time  
def OutputResults():
    with open('output_agent.csv','w',newline='') as outfile:
        writer=csv.writer(outfile)
        writer.writerow(['agent_id','from_origin_no_id','to_destination_node_id',
                         'departure_time_in_min','arrive_time_in_min','travel_time_in_min',
                         'path_node_seq_no','number_of_nodes'])
        for i in range(g_number_of_agents):
            agent=g_agent_list[i]
            agent.FieldCaculation()
            line=[agent.agent_id,agent.from_origin_node_id,agent.to_destination_node_id,
                  agent.departure_time_in_min,agent.arrive_time_in_min_in_assignment,
                  agent.travel_time_in_min_in_assignment,agent.path_node_seq_no,
                  agent.number_of_nodes]
            writer.writerow(line)
            
      
# In[1] caculate shortest path for any od pairs at any time     
if __name__=='__main__':
    start_time=datetime.datetime.now()
    read_input_data()
    TrafficAssignment()
    OutputResults()
    end_time=datetime.datetime.now()
    time_spend=end_time-start_time
    print('total time spend is '+str(time_spend))
    

        
    
    


    

    




    

   






    

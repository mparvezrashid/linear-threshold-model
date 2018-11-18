
# coding: utf-8

# In[75]:


import networkx as nx
import matplotlib.pyplot as plt
import random
import math


G = nx.fast_gnp_random_graph(10, .2, 1, directed=True)
for (u,v,w) in G.edges(data=True):
    w['weight'] = random.randint(0,10)
for v in G.nodes():
    var = G.in_degree(v,weight='weight')
    #print(var) #var contains the sum of incoming edge weights 
    for u, v, data in G.in_edges(v, data=True):
        #print (u,v,data)
        if(var!=0):
            G[u][v]['weight']=G[u][v]['weight']/var #normalizing weights for incoming edges
        #print (u,v,data) #to check the nomalize weights   
    #print(".................................")          
nx.set_node_attributes(G, 'Active', 0) #'Active' attribute is for diffusion or activating a node
G.node[1]['Active'] = 1 #Example: node 1 is set to active
G.add_edge(1, 2, weight=3)#Example: Add edge with weight
#print(G.node)
#print(G.edge)    
nx.draw_networkx(G, pos=None, arrows=True, with_labels=True)
plt.draw()


# In[ ]:





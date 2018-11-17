
# coding: utf-8

# In[37]:


import networkx as nx
import matplotlib.pyplot as plt
import random

#G = nx.Graph()
G = nx.fast_gnp_random_graph(10, .2, 1, directed=True)
#G.add_edge(1, 2) # default edge data=1
#G.add_edge(2, 3, weight=0.9) # specify edge data
#nx.draw(G)
for (u,v,w) in G.edges(data=True):
    w['weight'] = random.randint(0,10)
#for v in G.nodes:
    #var = G.in_degree(v,weight='weight')
    

G.in_degree(1,weight='weight')
print(G.edge)    
nx.draw_networkx(G, pos=None, arrows=True, with_labels=True)
plt.draw()


# In[ ]:





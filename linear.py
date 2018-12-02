import networkx as nx
import matplotlib.pyplot as plt
import random
import copy

def main():
    G = nx.fast_gnp_random_graph(100, .2, 1, directed=True)
    for (u,v,w) in G.edges(data=True):
        w['weight'] = random.randint(0,1)
    for v in G.nodes():
        var = G.in_degree(v,weight='weight')
        #print(var) #var contains the sum of incoming edge weights
        for u, v, data in G.in_edges(v, data=True):
            #print (u,v,data)
            if(var!=0):
                G[u][v]['weight']=G[u][v]['weight']/var #normalizing weights for incoming edges
            # print (u,v,data) #to check the nomalize weights
        #print(".................................")
    # nx.set_node_attributes(G, 'Active', 0) #'Active' attribute is for diffusion or activating a node
    # G.node[1]['Active'] = 1 #Example: node 1 is set to active
    # G.add_edge(1, 2, weight=0.3)#Example: Add edge with weight
    # print(/G.node)
    # print(G.edge)
    nx.draw_networkx(G, pos=None, arrows=True, with_labels=True)
    plt.draw()
    plt.savefig("examples.png")
    # the source nodes that we can activate
    arr = [1, 3, 4, 7, 8, 10, 14, 16, 20, 25, 41, 49]
    # simulation for 1000 rounds
    result = simulation(G, arr, simulationRound=1000);
    print(result);

def simulation(G, seeds, simulationRound):
    avg = 0;
    for k in range(simulationRound):
        layers = linear_threshold(G,seeds);
        # print(layers)
        # print(len(layers)) #the steps\
        count = 0
        for i in layers:
            count += len(i)
        #     print(len(i),end = ' ') #the size of avtivate node in each diffusion round
        # print(""); #change line
        # print(count) #the total number of activate nodes after all diffusion process
        avg += count;
        k += 1;
    return avg/simulationRound;

def linear_threshold(G, seeds):

  # make sure the seeds are in the graph
  for s in seeds:
    if s not in G.nodes():
      raise Exception("seed", s, "is not in graph")

  # copy the graph
  DG = copy.deepcopy(G)

  # init thresholds
  for n in DG.nodes():
    DG.node[n]['threshold'] = random.randint(0,1)

  # perform diffusion
  A = copy.deepcopy(seeds)
  # perform diffusion until no more nodes can be activated
  return _diffuse_all(DG, A)

def _diffuse_all(G, A):
  layer_i_nodes = [ ]
  layer_i_nodes.append([i for i in A])
  while True:
    len_old = len(A)
    A, activated_nodes_of_this_round = _diffuse_one_round(G, A)
    layer_i_nodes.append(activated_nodes_of_this_round)
    if len(A) == len_old:
      break
  return layer_i_nodes

# activate neighbors according to threshold and in-degree weights
def _diffuse_one_round(G, A):
  activated_nodes_of_this_round = set()
  for s in A:
    nbs = G.successors(s)
    for nb in nbs:
      if nb in A:
        continue
      active_nb = list(set(G.predecessors(nb)).intersection(set(A)))
      if _influence_sum(G, active_nb, nb) >= G.node[nb]['threshold']:
        activated_nodes_of_this_round.add(nb)
  A.extend(list(activated_nodes_of_this_round))
  return A, list(activated_nodes_of_this_round)

# Calculate the in-degree sum of weights
def _influence_sum(G, froms, to):
  influence_sum = 0.0
  for f in froms:
    influence_sum += G[f][to]['weight']
  return influence_sum



if __name__ == "__main__":
    main()
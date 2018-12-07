import networkx as nx
import matplotlib.pyplot as plt
import random
import copy
import time
import numpy as np
import math
from itertools import combinations


NODES_NUM = 10  
SOURCE_NODES = 3 # k nodes
EDGES_SELECT = 3 # m edge


def main():
    G = nx.fast_gnp_random_graph(NODES_NUM, 0.2, 1, directed=True)
    for (u, v, w) in G.edges(data=True):
        w['weight'] = random.randint(0, 10)

    # all weighted edges
    all_edges = list(permut(NODES_NUM, 2))

    potential_edge_size = NODES_NUM * (NODES_NUM - 1) - G.number_of_edges()
    potential_edge_set = set(all_edges) - G.edges()

    potenial_edge_weights = []
    edge_dic = {}
    for x in potential_edge_set:
        w = random.randint(0, 10)
        potenial_edge_weights.append((*x, w))

    nx.draw_networkx(G, pos=None, arrows=True, with_labels=True)
    plt.draw()
    plt.savefig("examples.png")
    print(G.nodes)
    selectEdges(EDGES_SELECT, potenial_edge_weights, G)





def simulation(G, seeds, simulationRound):
    avg = 0;
    for k in range(simulationRound):
        layers = linear_threshold(G,seeds);
        # print(layers)
        # print(len(layers)) #the steps\
        count = 0
        for i in layers:
            count += len(i)
            # print(len(i),end = ' ') #the size of avtivate node in each diffusion round
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
    DG.node[n]['threshold'] = random.randint(1,10)/10;

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


def permut(n, k):
    '''
    cn(k)
    n: size of array to be permutated
    k: number of edges to be selected
    returns: 2D array
    '''
    from itertools import permutations

    return permutations(range(n), k)


def reweight(G):
    '''
    after adding edges with unnormalized weight, G needs to be normalized
    '''

    for v in G.nodes():
        var = G.in_degree(v, weight='weight')
        # print(var) #var contains the sum of incoming edge weights
        for u, v, data in G.in_edges(v, data=True):
            # print (u,v,data)
            if (var != 0):
                G[u][v]['weight'] = G[u][v]['weight'] / var  # normalizing weights for incoming edges
            # print (u,v,data) #to check the nomalize weights
        # print(".................................")


def selectEdges(k, wl, G):
    '''
    k: number of edges to be selected
    wl: the potential weight list (triples) where all weights are defined
    G: the graph to be added weight with
    '''
    from itertools import combinations
    start = time.time()
    l = np.array(wl, dtype='i,i,i')
    print(l)

    all_combi_edges = list(combinations(list(range(len(wl))), k))

    i = 0
    for c in all_combi_edges:
        selected = l[list(all_combi_edges[i])]
        print("iteration: ", i, " selected: ", selected)

        G_new = G.copy()
        G_new.add_weighted_edges_from(selected)
        reweight(G_new)
        i += 1
        # the number of source nodes that we can activate
        # generate all possible combinations of source nodes
        comb = combinations(G_new.nodes(), SOURCE_NODES)
        # simulate 1000 times for each solution
        # (1,2,3,4) -> [1,2,3,4]
        # max = 0
        for input in list(comb):
            # print(input)
            a = []
            for nodes in tuple(input):
                a.append(nodes)
            print(a)
            result = simulation(G_new, a, simulationRound=1000);
            # max = Math.max(max, result)
            print(result)
        # print(max)

if __name__ == "__main__":
    main()

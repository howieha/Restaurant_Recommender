# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:27:32 2020
@author: wchhuang
"""
import networkx as nx
from louvain import louvain_partition, plot_partitions_FR
import networkx.algorithms.shortest_paths.weighted as spw
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle


def ranking(network, partition):
    """
    Parameters
    ----------
    network : network result from louvain.
    partition : partition result from louvain.

    Returns
    -------
    rep : LIST. List of representatives in each sub-network.
    subg : LIST. List of sub-graphs for each sub-network.
    pr : LIST. List of dicts for each sub-network, on node weights.
    """

    subg_num = max(partition.values()) + 1      # PARTITIONED SUBGRAPH NUMBER
    # SUBGRAPH DIVISION
    subg = [None] * subg_num
    for subi in range(subg_num):
        subg[subi] = nx.subgraph(network,
                             [x for x in networkp.nodes()
                              if partitionp[x] == subi])
    # PAGERANK WITH EDGE WEIGHTS
    pr  = [nx.pagerank(subi) for subi in subg]
    # REPRESENTATIVE FOR EACH SUBGRAPH
    rep = [max(pri, key=lambda key: pri[key]) for pri in pr]

    return rep, subg, pr


def prplot(subnetworks, sub_id, PR_result):
    """
    Parameters
    ----------
    subnetworks (subg): LIST. List of sub-graphs for each sub-network.
    sub_id : INT. Subgraph ID.
    PR_result (pr): LIST. List of dicts for each sub-network, on node weights.

    Returns
    -------
    fig : FIGURE.
    """
    subg = subnetworks[sub_id]      # SUB-NETWORK FOR PLOTTING
    pos  = nx.spring_layout(subg)   # PLOT POSITIONs
    fig = plt.figure(figsize=(6, 6))

    node_weight = list(PR_result[sub_id].values())      # NODE WEIGHTS
    edge_weight = [subg[u][v]['weight'] for u, v in subg.edges()]   # EDGE WEIGHTS

    nx.draw_networkx_nodes(subg, pos, node_size=80,
                           node_color=node_weight, cmap=cm.Reds)
    nx.draw_networkx_edges(subg, pos,
                           width=edge_weight, alpha=0.3)
    nx.draw_networkx_labels(subg, pos, font_size=8)
    plt.show()

    return fig


def dist(subnetworks, node_id, path_method='dijkstra'):
    """
    Parameters
    ----------
    subnetworks (subg): LIST. List of sub-graphs for each sub-network.
    node_id : INT. Source node ID for calculating in-group distances.
    path_method : CATEGORICAL ('dijkstra', 'bellman_ford'), default = 'dijkstra'.

    Returns
    -------
    sorted_distances : DICT. In-group nodes and sorted distances.
    """

    # FIND SUBGRAPH FOR node_id
    subgi = [node_id in subnetworks[i] for i in range(len(subnetworks))]
    subi  = next(i for i, v in enumerate(subgi) if v)
    if path_method == 'dijkstra':
        node_distances = spw.single_source_dijkstra_path_length(subnetworks[subi], node_id)
    elif path_method == 'bellman_ford':
        node_distances = spw.single_source_bellman_ford_path_length(subnetworks[subi], node_id)
    else:
        raise ValueError('Invalid shortest path algorithm.')
        return
    # SORT BY DISTANCE
    sorted_distances = {k: v for k, v in \
                        sorted(node_distances.items(), key=lambda x: x[1])}
    return sorted_distances



if __name__ == "__main__":
    # LOAD DATA FROM PICKLE
    pctot = pickle.load(open("pctot.p", "rb"))      # PEARSON, OVERALL
    networkp, partitionp = louvain_partition(pctot) # LOUVAIN PARTITIONING

    # PLOT PARTITIONING FIGURE
    plot_partitions_FR(networkp, partitionp)

    # CONDUCT PAGERANK AND PLOT FOR SUBNETWORK 2
    repp, subgp, prp = ranking(networkp, partitionp)
    fig2 = prplot(subgp, sub_id=2, PR_result=prp)

    # COMPUTE NODE DISTANCES FOR NODE 172
    dist172 = dist(subgp, 172)

    # COMPUTE NODE DISTANCE FOR ALL NODES
    nodelists = [dist(subgp, nodei) for nodei in range(len(pctot))]
    pickle.dump(nodelists, open("distances.p", "wb"))
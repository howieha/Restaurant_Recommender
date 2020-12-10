# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:27:32 2020
@author: wchhuang
"""
import networkx as nx
import numpy as np
from louvain import louvain_partition, plot_partitions_FR
import networkx.algorithms.shortest_paths.weighted as spw
import matplotlib.pyplot as plt
from matplotlib import cm
import loadcsv
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
    fig  = plt.figure(figsize=(6, 6))

    node_weight = list(PR_result[sub_id].values())      # NODE WEIGHTS
    edge_weight = [subg[u][v]['weight'] for u, v in subg.edges()]   # EDGE WEIGHTS

    nx.draw_networkx_nodes(subg, pos, node_size=80,
                           node_color=node_weight, cmap=cm.Reds)
    nx.draw_networkx_edges(subg, pos,
                           width=edge_weight, alpha=0.3)
    nx.draw_networkx_labels(subg, pos, font_size=8)
    plt.show()

    return fig


def gdist(replist, path_method='dijkstra', filename='pctot_raw.p'):
    """
    Parameters
    ----------
    replist (rep): LIST. List of representatives in each sub-network.
    path_method : CATEGORICAL ('dijkstra', 'bellman_ford'), default = 'dijkstra'.
    filename : STRING, default = 'pctot_raw.p'. Filename of raw corr coeff matrix.

    Returns
    -------
    gr_dist (inter_group_dist): DICT. Gives group-to-group distances.
    """

    # LOAD RAW CORR MATRIX
    pctot_raw = pickle.load(open("pctot_raw.p", "rb"))
    # FILTER GROUP REPRESENTATIVES
    pc_group  = pctot_raw[replist, :][:, replist]
    pc_group  = np.absolute(pc_group)
    # FORM INTERGROUP DISTANCE
    nx_group  = nx.from_numpy_array(pc_group)
    if path_method == 'dijkstra':
        gr_dist = dict(spw.all_pairs_dijkstra_path_length(nx_group))
    elif path_method == 'bellman_ford':
        gr_dist = dict(spw.all_pairs_bellman_ford_path_length(nx_group))
    else:
        raise ValueError('Invalid shortest path algorithm.')
        return
    return gr_dist


def dist(subnetworks, node_id,
         path_method='dijkstra',
         inter_group=False, inter_group_dist=None, rep_dist=None):
    """
    Parameters
    ----------
    subnetworks (subg): LIST. List of sub-graphs for each sub-network.
    node_id : INT. Source node ID for calculating in-group distances.
    path_method : CATEGORICAL ('dijkstra', 'bellman_ford'), default = 'dijkstra'.
    inter_group : BOOLEAN, default = False. Indicate whether or not calculate inter-group distances.
    inter_group_dist : DICT. Gives group-to-group distances.
    rep_dist : DICT. Gives in-group distances within each group to their representatives.

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
    # INCLUDE INTER_GROUP DISTANCES
    if inter_group:
        # BASELINE MULTIPLIER
        basedist = dict({(i, subnetworks[subi].number_of_nodes() * v)
                         for i, v in inter_group_dist[subi].items()})
        # ADDING INTERGROUP DISTANCES
        for subj in range(len(subnetworks)):
            if subj != subi:
                distj = dict({(i, basedist[subj] + v)
                         for i, v in rep_dist[subj].items()})
                node_distances.update(distj)

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
    repdists  = [dist(subgp, nodei) for nodei in repp]  # in-group dists
    gdists    = gdist(repp)                             # btw-group dists
    # WITHOUT INTERGROUP
    nodelists = [dist(subgp, nodei) for nodei in range(len(pctot))]
    # WITH INTERGROUP
    nodelists_intergroup = [dist(subgp, nodei,
                                 inter_group=True,
                                 inter_group_dist=gdists, rep_dist=repdists)
                            for nodei in range(len(pctot))]


    # LOAD ENV SETUP
    from envinit import Dataset
    db = pickle.load(open("db.p", "rb"))

    # RETRIEVE BUSINESS IDS
    df_business = loadcsv.loadcsv('business', db.data['business'])
    dict_busn_id = df_business.loc[:, 'business_id']
    dict_busn_id = dict_busn_id.to_dict()

    for nodei in range(len(nodelists)):
        listi  = nodelists[nodei]       # ORIGINAL DICTIONARY OF DISTANCE
        newlst = dict((dict_busn_id[key], value)
                      for (key, value) in listi.items())    # NEW DICT
        nodelists[nodei] = newlst       # UPDATE

    for nodei in range(len(nodelists_intergroup)):
        listi  = nodelists_intergroup[nodei]
        newlst = dict((dict_busn_id[key], value)
                      for (key, value) in listi.items())    # NEW DICT
        nodelists_intergroup[nodei] = newlst                # UPDATE

    # UPDATE OUTER LOOP ID
    nodelists_id = dict(zip(list(dict_busn_id.values()),
                            nodelists))
    nodelists_intergroup_id = dict(zip(list(dict_busn_id.values()),
                                       nodelists_intergroup))
    pickle.dump(nodelists_id, open("distances.p", "wb"))
    pickle.dump(nodelists_intergroup_id, open("distances_interg.p", "wb"))
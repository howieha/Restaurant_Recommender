
import numpy as np
import community as comm
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn import datasets



def louvain_partition(network, random_seed=999):
    """
    :param network: The network's adjacency matrix representation in Numpy Array format
    :return network_new: The network's representation in Networkx format
    :return partition:  The network's partition in a dict
    """

    network_new = nx.from_numpy_array(network)
    partition = comm.best_partition(network_new, random_state=random_seed)
    return network_new, partition

def plot_partitions_FR(network, partition):
    """
    Plot the partitions using Fruchterman-Reingold force-directed algorithm
    :param network: The networkx network representation
    :param partition: Network partition represented by a dict
    """
    pos = nx.spring_layout(network)
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    groups_id = list(partition.values())

    nx.draw_networkx_nodes(network, pos, partition.keys(), node_size=40, cmap=cmap, node_color=groups_id)

    edge_color_list = [groups_id[i[0]]for i in network.edges()]
    nx.draw_networkx_edges(network, pos, alpha=0.3, cmap=cmap, edge_color=edge_color_list)
    plt.show()



if __name__ == "__main__":

    # s1 = np.random.rand(20, 2)
    # s2 = np.random.rand(20, 2) + 1
    # s3 = np.random.rand(20, 2) + 2
    # s4 = np.random.rand(20, 2) + 3
    # s5 = np.random.rand(20, 2) + 4
    # a = np.concatenate((s1, s2, s3, s4, s5), axis=0)
    # a = np.matmul(a, a.T)
    # print(a.shape)




    a = datasets.make_spd_matrix(100)
    a = np.absolute(a)
    a[a<0.02] = 0
    print(a)

    network, partition = louvain_partition(a)
    # print(network.edges())
    # print(partition.values())
    plot_partitions_FR(network, partition)






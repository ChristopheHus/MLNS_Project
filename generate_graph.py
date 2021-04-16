import networkx as nx
import numpy as np

path_csv = r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013-names.csv"
path = r"D:\Documents\CS_3A\MLNS\Projet\chosen_nodes.txt"
path_graph = r"D:\Documents\CS_3A\MLNS\Projet\graph-2013.txt"



def s2data(s):
    # day 0-30 A-_
    # hour 0-23 A-X
    # count int
    days = s.split(",")

    def read_day(day):
        nd = ord(day[0]) - 65
        hours = [0]*24
        current_hour = 0
        for c in day[1:]:
            if c.isnumeric():
                hours[current_hour] = hours[current_hour]*10 + ord(c)-48
            else:
                current_hour = ord(c) - 65
        return nd, hours

    L = np.zeros(24*31)
    for day in days:
        if len(day) == 0: continue
        nd, hours = read_day(day)
        L[nd*24:(nd+1)*24] = hours

    return L



def getNodes():
    names = {}
    with open(path, encoding="utf8") as f:
        for l in f:
            if l[0] == "#": continue
            data = l[:-1].split(" ")
            names[data[1]] = s2data(data[3])

    nodes = set()
    with open(path_csv, encoding="utf8") as f:
        next(f)
        for l in f:
            i = l.find(",")
            node = int(l[:i])
            name = l[i+1:].strip("\"\n").replace(" ", "_")

            if name in names:
                nodes.add(node)

    names2id = {}
    for i,name in enumerate(names):
        names2id[name] = i
    nodes2id = {}
    for i,node in enumerate(nodes):
        nodes2id[node] = i

    return names, list(nodes), names2id, nodes2id


N = 24*31
names, nodes, names2id, nodes2id = getNodes()


graph = nx.Graph()
graph.add_nodes_from([(node, {"name":name[0],"views":name[1]}) for name,node in zip(names.items(), nodes)])


with open(path_graph, encoding="utf8") as f:
    for l in f:
        if l[0] == "#": continue

        nodei, nodej = l[:-1].split(" ")
        nodei, nodej = int(nodei), int(nodej)

        graph.add_edge(nodei, nodej)


graph.remove_nodes_from(list(nx.isolates(graph)))


import matplotlib.pyplot as plt

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    print("spring")
    pos = nx.spring_layout(graph)
    print("nodes")
    nx.draw_networkx_nodes(graph,pos)
    print("edges")
    nx.draw_networkx_edges(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

save_graph(graph,"my_graph.png")



from scipy.sparse import csr_matrix, lil_matrix
W = nx.adjacency_matrix(graph)
W = W + W.transpose()
rows, cols = W.nonzero()

id2node = list(graph.nodes)
W2 = lil_matrix(W.shape)


def compare(a, b):
    an0 = a.nonzero()
    bn0 = b.nonzero()

    c = np.intersect1d(an0, bn0, assume_unique=True)

    ret = np.stack((a[c],b[c]), axis=1)
    ret = ret.min(axis=1) / ret.max(axis=1)
    return np.where(ret>.5, ret, 0).sum()

for i in rows:
    for j in cols:
        if i>j:
            W2[i,j] = compare(graph.nodes[id2node[i]]["views"], graph.nodes[id2node[j]]["views"])
W2 = W2 + W2.transpose()

#W = W + W.transpose()

rows, cols = W2.nonzero()
for i in rows:
    for j in cols:
        W2[i,j] = W2[i,j] if W2[i,j]>300 else 0

W2.eliminate_zeros()


def activation(x, θ=0.):
    return 1 if x>θ else -1
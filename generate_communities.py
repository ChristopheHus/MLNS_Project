import networkx as nx
import numpy as np

path = r"D:/Documents/CS_3A/MLNS/Projet/trained_graph.txt"
N = 76554

graph = nx.Graph()
graph.add_nodes_from(range(N))

with open(path) as f:
    for l in f:
        i, j, w = l[:-1].split(" ")
        i, j, w = int(i), int(j), float(w)

        if w>300:
            graph.add_edge(i,j,attr={"w":w})

giant = graph.subgraph(max(nx.connected_components(graph), key=len))

from networkx.algorithms import community
communities_generator = community.girvan_newman(giant)

top_lvl = next(communities_generator)




with open(path) as f:
    with open(path[:-4]+"_0.txt", "w") as f2:
        for l in f:
            i, j, w = l[:-1].split(" ")
            i, j, w = int(i), int(j), float(w)

            if w>300:
                f2.write(f"{i} {j}\n")


with open(r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013-names.csv", encoding="utf8") as f:
    tofind = [1177344]
    next(f)
    for l in f:
        i = l.find(",")
        node = int(l[:i])
        name = l[i+1:].strip("\"\n")

        if node in tofind:
            print(f"{node} : {name}")


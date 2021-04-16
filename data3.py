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
    names = set()
    with open(path, encoding="utf8") as f:
        for l in f:
            if l[0] == "#": continue
            data = l[:-1].split(" ")
            names.add(data[1])

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

    return list(names), list(nodes), names2id, nodes2id


N = 24*31
names, nodes, names2id, nodes2id = getNodes()

hours = np.zeros((len(nodes), N))
with open(path, encoding="utf8") as f:
    for l in f:
        if l[0] == "#": continue
        data = l[:-1].split(" ")
        hours[names2id[data[1]]] = s2data(data[3])


graph = {}
with open(path_graph, encoding="utf8") as f:
    for l in f:
        if l[0] == "#": continue

        nodei, nodej = l[:-1].split(" ")
        nodei, nodej = nodes2id[int(nodei)], nodes2id[int(nodej)]

        if nodei in graph:
            graph[nodei][nodej] = 0
        else:
            graph[nodei] = {nodej: 0}



def sim(i, j, t):
    if hours[i,t]==0 or hours[j,t]==0:
        return 0
    return min(hours[i,t], hours[j,t]) / max(hours[i,t], hours[j,t])


for t in range(N):
    for i in graph:
        for j in graph[i]:
            dw = sim(i,j,t)
            graph[i][j] += dw if dw>.5 else 0


path_save_graph = r"D:\Documents\CS_3A\MLNS\Projet\trained_graph.txt"
with open(path_save_graph, "w", encoding="utf8") as f:
    for i in graph:
        for j in graph[i]:
            f.write(str(i)+" "+str(j)+" "+str(graph[i][j])+"\n")
path_save_nodes = r"D:\Documents\CS_3A\MLNS\Projet\trained_nodes2id.txt"
with open(path_save_nodes, "w", encoding="utf8") as f:
    for node in nodes2id:
        f.write(str(node)+" "+str(nodes2id[node])+"\n")


sym_graph = {}
for i in graph:
    for j in graph[i]:
        if i in sym_graph:
            sym_graph[i][j] = graph[i][j]
        else:
            sym_graph[i] = {j:graph[i][j]}

w_max = 0
w_min = 0
for i in graph:
    for j in graph[i]:
        w_max = max(w_max, graph[i][j])
        w_min = min(w_min, graph[i][j])


hist = [0]*19
for i in graph:
    for j in graph[i]:
        hist[int(graph[i][j]//30)] += 1


μ = hours.mean(axis=1).reshape((-1,1))
σ = hours.std(axis=1).reshape((-1,1))
n = 5
P0 = np.where(hours > n*σ + μ, 1, -1)

def pre_step(P):
    Q = np.zeros_like(P, dtype=float)
    for i in graph:
        for j in graph[i]:
            Q[j] += graph[i][j]*P[i]
    return Q

θ = 0.
def step(P):
    Q = np.zeros_like(P, dtype=float)
    for i in graph:
        for j in graph[i]:
            Q[j] += graph[i][j]*P[i]
    Q = np.where(Q>θ, 1, -1)
    print(np.abs(P-Q).sum())
    return Q

P = P0
Q = step(P)
while np.abs(P-Q).sum() > 0:
    Q, P = step(Q), Q
path_csv = r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013-names.csv"
path = r"D:\Documents\CS_3A\MLNS\Projet\chosen_nodes.txt"
path_graph = r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013.txt"
path_graph2 = r"D:\Documents\CS_3A\MLNS\Projet\graph-2013.txt"

def burstiness(s, n=5):
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

    tmp = L.mean() + n*L.std()
    return np.where(L>tmp, 1, 0).sum()


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

with open(path_graph, encoding="utf8") as f:
    with open(path_graph2, "w", encoding="utf8") as f2:
        for l in f:
            if l[0]=="#":
                f2.write(l)
                continue

            nodei, nodej = l[:-1].split(" ")
            nodei, nodej = int(nodei), int(nodej)

            if nodei in nodes and nodej in nodes:
                f2.write(l)
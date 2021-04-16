path = r"D:\Documents\CS_3A\MLNS\Projet\pagecounts-2018-01-views"
path2 = r"D:\Documents\CS_3A\MLNS\Projet\pagecounts-2018-01-views_pruned"
path_csv = r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013-names.csv"
path_chosen = r"D:\Documents\CS_3A\MLNS\Projet\chosen_nodes.txt"


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


with open(path2, encoding="utf8", errors="surrogateescape") as file:
    with open(path_chosen, "w", encoding="utf8") as f:
        for s in file:
            s = s[:-1]
            if s[0]=="#":
                f.write(s+"\n")
                continue

            data = s.split(" ")
            count = int(data[2])

            if count>=500:
                b = burstiness(data[3])
                if b>5:
                    f.write(s+"\n")



with open(path2, encoding="utf8", errors="surrogateescape") as file:
    with open(path_chosen, "w", encoding="utf8") as f2:
        for s in file:
            s = s[:-1]
            if s[0]=="#": continue

            data = s.split(" ")
            count = int(data[2])

            if count>=200:
                f2.write(data[1]+"\n")


hist = [0 for i in range(1438)]

with open(path2, encoding="utf8", errors="surrogateescape") as file:
    for s in file:
        s = s[:-1]
        if s[0]=="#": continue

        data = s.split(" ")
        count = int(data[2])

        hist[int(50*np.log2(count))] += 1

print("min ", min_c)
print("max ", max_c)
print("mean ", mean_c[0]/mean_c[1])



names = {}

with open(path_csv, encoding="utf8") as f:
    next(f)
    for l in f:
        i = l.find(",")
        id, name = l[:i], l[i+1:]
        name = name.strip("\"\n")
        names[name.replace(" ","_")] = 0



#latin-1
with open(path, encoding="utf8", errors="surrogateescape") as file:
    with open(path2, mode="w", encoding="utf8") as f2:
        for i, line in enumerate(file):
            if line[0] == "#":
                f2.write(line)
                continue

            l = line.split(" ")

            if l[1] in names:
                names[l[1]] = 1
                f2.write(line)


if False:
    if False:
        for i, line in enumerate(file):
            if line[0] == "#":
                f2.write(line)
            else:
                l = line.split(" ")
                #if l[2].isnumeric():
                #    count = int(l[2])
                #elif l[1].isnumeric():
                #    count = int(l[1])
                #else:
                #    count = 0

                if not(l[1].startswith("File:")) and not(l[1].startswith("Special:")) and not(l[1].startswith("Category:")) and not(l[1].startswith("User:")) and not(l[1].startswith("User_talk:")):
                    f2.write(line)



    with open(path, encoding="utf8", errors="surrogateescape") as file:
        L = set()
        for line in file:
            if line[0] == "#":
                continue
            title = line.split(" ")[1]
            if "Alexander" in title and "Seton" in title:
                L.add(title)

        print(L)

    raise Exception
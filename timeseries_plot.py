import numpy as np



def plot_line(n):
    path = r"D:\Documents\CS_3A\MLNS\Projet\chosen_nodes.txt"

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

    with open(path, encoding="utf8") as f:
        k = 0
        for l in f:
            if l[0] == "#": continue
            if k==n:
                data = l[:-1].split(" ")
                print(data[1])
                data = s2data(data[3])
                break
            k += 1

    print(data.sum())
    plt.plot(data)
    n = 5
    μ = data.mean()
    σ = data.std()
    mask = np.where(data>n*σ+μ, 1, 0)
    plt.plot(data*mask)
    plt.show()
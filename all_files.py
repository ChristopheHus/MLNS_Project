#Note: to generate the plot for the graphs we used Graphia as networkx was too slow to compute the plot in 1hour
#https://graphia.app/

import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
from numpy.lib import i0


path_pageviews = r"D:\Documents\CS_3A\MLNS\Projet\pagecounts-2018-01-views"
path_csv = r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013-names.csv"
path_hl_graph = r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013.txt"


#generate the stripped version of the page view dataset
names2node = {}
with open(path_csv, encoding="utf8") as f:
	next(f)
	for l in f:
		i = l.find(",")
		node = int(l[:i])
		name = l[i+1:].strip("\"\n").replace(" ", "_")

		if name not in names2node:
			names2node[name] = node


path_pageviews_pruned = r"D:\Documents\CS_3A\MLNS\Projet\pagecounts-2018-01-views_pruned"
with open(path_pageviews, encoding="utf8") as f:
	with open(path_pageviews_pruned, "w", encoding="utf8") as f2:
		for l in f2:
			if l[0] == "#":
				f2.write(l)
				continue
			
			data = l[:-1].split(" ")
			#project_type, page_name, monthly_views, views_per_hour_serialized
			if data[1] in names2node:
				f2.write(l)



# remove pages with to small amount of views or burstiness
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

path_pageviews_stripped = r"D:\Documents\CS_3A\MLNS\Projet\chosen_nodes.txt"
with open(path_pageviews_pruned, encoding="utf8", errors="surrogateescape") as file:
	with open(path_pageviews_stripped, "w", encoding="utf8") as f:
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

# to generate the histogram 
hist = [0 for i in range(1438)]
with open(path_pageviews_stripped, encoding="utf8", errors="surrogateescape") as file:
	for s in file:
		s = s[:-1]
		if s[0]=="#": continue

		data = s.split(" ")
		count = int(data[2])

		hist[int(50*np.log2(count))] += 1
plt.plot([2**(i/50) for i in range(1438)], hist)
plt.show()




#remove the edges with non existant nodes
names = set()
with open(path_pageviews_stripped, encoding="utf8") as f:
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

path_graph2 = r"D:\Documents\CS_3A\MLNS\Projet\graph-2013.txt"
with open(path_hl_graph, encoding="utf8") as f:
	with open(path_graph2, "w", encoding="utf8") as f2:
		for l in f:
			if l[0]=="#":
				f2.write(l)
				continue

			nodei, nodej = l[:-1].split(" ")
			nodei, nodej = int(nodei), int(nodej)

			if nodei in nodes and nodej in nodes:
				f2.write(l)



# function to plot the hourly views of the line n in the file @ path
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





#parse the serialized hourly views
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

def getNodes(path):
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

# calculate the weights of the Hopefield network
N = 24*31
names, nodes, names2id, nodes2id = getNodes(path_pageviews_stripped)

hours = np.zeros((len(nodes), N))
with open(path_pageviews_stripped, encoding="utf8") as f:
	for l in f:
		if l[0] == "#": continue
		data = l[:-1].split(" ")
		hours[names2id[data[1]]] = s2data(data[3])


graph = {}
with open(path_graph2, encoding="utf8") as f:
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







#find the names of a given list of node
def find(tofind):
	with open(path_csv, encoding="utf8") as f:
		next(f)
		for l in f:
			i = l.find(",")
			node = int(l[:i])
			name = l[i+1:].strip("\"\n")

			if node in tofind:
				print(f"{node} : {name}")



#generate the communities, really slow
graph = nx.Graph()
graph.add_nodes_from(range(N))

with open(path_save_graph) as f:
	for l in f:
		i, j, w = l[:-1].split(" ")
		i, j, w = int(i), int(j), float(w)

		if w>300:
			graph.add_edge(i,j,attr={"w":w})

giant = graph.subgraph(max(nx.connected_components(graph), key=len))

from networkx.algorithms import community
communities_generator = community.girvan_newman(giant)

top_lvl = next(communities_generator)
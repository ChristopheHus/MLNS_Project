#https://dumps.wikimedia.org/other/pagecounts-ez/merged/
path = r"D:\Documents\CS_3A\MLNS\Projet\pagecounts-2018-01-views"
path2 = r"D:\Documents\CS_3A\MLNS\Projet\pagecounts-2018-01-views_pruned"
path_csv = r"D:\Documents\CS_3A\MLNS\Projet\enwiki-2013-names.csv"


def get_names(path_csv):
	names = {}

	with open(path_csv, encoding="utf8") as f:
		next(f)
		for l in f:
			i = l.find(",")
			id, name = l[:i], l[i+1:]
			name = name.strip("\"\n")
			names[name.replace(" ","_")] = 0
	
	return names


def preprocess_data(in_path, out_path, csv_path):
	names = get_names(csv_path)

	with open(in_path, encoding="utf8", errors="surrogateescape") as file:
		with open(out_path, mode="w", encoding="utf8") as f2:
			for i, line in enumerate(file):
				if line[0] == "#":
					f2.write(line)
					continue
					
					l = line.split(" ")

					if l[1] in names:
						names[l[1]] = 1
						f2.write(line)
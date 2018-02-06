import networkx as nx 
from community2vec import Commmunity2Vec
import os
import pickle

folder = r'../../IIITD_work/Data/CoAuthorship'

# g = nx.Graph()

# # print(os.path.join(folder, 'coauthorship_network.txt'))
# try:
# 	f = open(os.path.join(folder, 'coauthorship_network.txt'))
# 	lines= f.read().split('\n')
# 	for l in lines:
# 		nodes = list(filter(('').__ne__, l.split('\t')))
# 		if nodes[0] not in g.nodes.keys():
# 			g.add_node(nodes[0])
# 		if nodes[1] not in g.nodes.keys():
# 			g.add_node(nodes[1])
# 		g.add_edge(nodes[0],nodes[1])
# 	print('Graph built....')
# 	communities = []
# 	fc = open(os.path.join(folder, 'coauthorship_community.txt'))
# 	lines = fc.read().split('\n')
# 	for l in lines:
# 		communities.append(list(filter(('').__ne__, l.split('\t'))))
# 	print(len(communities),len(lines),'Building community2vec model')
# 	c = Commmunity2Vec(g)
# 	c.build_community_from_list(communities)
# 	print('Building co-occurance matrix')
# 	c.build_community_co_occurance_matrix_edges()
# 	print('Building PMI matrix')
# 	c.create_PMIs()
# 	print('Building PPMI matrix')
# 	c.create_PPMIs()
# 	c.scale_PPMIs()
# 	print(c.communities.keys())
# 	print(c.get_vec('10'))
# except Exception as e:
# 	raise e
# finally:
# 	f.close()
# 	fc.close()

file = open("G:\IIITD_work\Data\CoAuthorship\combined.txt",encoding="utf-8")

data = {}
authors = []
topic = None
i = 0
errs = 0
try:
	while(True):
		x = file.readline()
		if x == '':
			break
		if x.startswith('#index'):
			if topic != None:
				if topic in data.keys():
					authors_in = data[topic]
					for author in authors:
						if author not in authors_in:
							authors_in.append(author)
				else:
					data[topic] = authors					
			i = (i + 1) % 10000
			authors = []
			topic = None
			if i == 0:
				print(file.tell())
		else:
			if x.startswith('#@'):
				x = x[2:]
				authors = x.split(',')
			elif x.startswith('#f'):
				topic = x[2:]
except Exception as e:
	print(e)
	errs += 1

file.close()

for toic in data.keys():
	print(toic, len(data[toic]))
	pickle.dump(data[toic],open(toic.strip()+'.p','wb'))
	
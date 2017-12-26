import networkx as nx 
from community2vec import Commmunity2Vec
import os

folder = r'../../IIITD_work/Data/CoAuthorship'

g = nx.Graph()

# print(os.path.join(folder, 'coauthorship_network.txt'))
try:
	f = open(os.path.join(folder, 'coauthorship_network.txt'))
	lines= f.read().split('\n')
	for l in lines:
		nodes = list(filter(('').__ne__, l.split('\t')))
		if nodes[0] not in g.nodes.keys():
			g.add_node(nodes[0])
		if nodes[1] not in g.nodes.keys():
			g.add_node(nodes[1])
		g.add_edge(nodes[0],nodes[1])
	print('Graph built....')
	communities = []
	fc = open(os.path.join(folder, 'coauthorship_community.txt'))
	lines = fc.read().split('\n')
	for l in lines:
		communities.append(list(filter(('').__ne__, l.split('\t'))))
	print(len(communities),len(lines),'Building community2vec model')
	c = Commmunity2Vec(g)
	c.build_community_from_list(communities)
	print('Building co-occurance matrix')
	c.build_community_co_occurance_matrix_edges()
	print('Building PMI matrix')
	c.create_PMIs()
	print('Building PPMI matrix')
	c.create_PPMIs()
	c.scale_PPMIs()
	print(c.communities.keys())
	print(c.get_vec('10'))
except Exception as e:
	raise e
finally:
	f.close()
	fc.close()
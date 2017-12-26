# Commmunity2Vec implementation

'''
need to add comments at each significant step
'''
import networkx as nx
import numpy as np
from scipy import spatial

class Commmunity2Vec(object):
	"""docstring for Commmunity2Vec"""
	def __init__(self, nx_G):
		self.graph = nx_G
		self.communities = None
		self.community_co_occ_mat = None
		self.PMI = None
		self.PPMI = None
		self.community_length = None

	def build_community_from_list(self,coms):
		_communities = {}
		i=0
		for community in coms:
			_communities[str(i)] = set(community)
			for node in community:
				if 'tags' in self.graph.nodes[node].keys():
					self.graph.nodes[node]['tags'] += [str(i)]
				else:
					self.graph.nodes[node]['tags'] = [str(i)]
			i+=1
		self.communities = _communities
		self.community_length = len(self.communities)
	def build_community_from_tags(self):
		_communities = {}
		for node in list(self.graph.nodes):
			if 'tags' in self.graph.nodes[node].keys():
				for com in self.graph.nodes[node]['tags']:
					if com not in _communities:
						_communities[com] = set([node])
					else:
						_communities[com].add(node)
		self.communities = _communities
		self.community_length = len(self.communities)

	def drop_insignificant_communities(self, threshold_size):
		coms = self.communities.keys()
		coms = list(coms)[:]
		for com in coms:
			if(len(self.communities[com])<threshold_size):
				self.communities.pop(com)
		self.community_length = len(self.communities)

	def build_community_co_occurance_matrix_overlap(self):
		com_keys = list(self.communities.keys())
		self.community_co_occ_mat = np.zeros((self.community_length,self.community_length))
		for i in range(self.community_length):
			for j in range(self.community_length):
				self.community_co_occ_mat[i,j] = len(self.communities[com_keys[i]].intersection(self.communities[com_keys[j]]))

	def build_community_co_occurance_matrix_edges(self):
		self.community_co_occ_mat = np.zeros((self.community_length,self.community_length))
		for edge in self.graph.edges():
			n1 = edge[0]
			n2 = edge[1]
			# print((n1,n2))
			try:
				c1 = self.graph.nodes[n1]['tags']
				c2 = self.graph.nodes[n2]['tags']
				# print(c1,c2)
				for c in c1:
					for cc in c2:
						self.community_co_occ_mat[int(c),int(cc)] += 1
						self.community_co_occ_mat[int(cc),int(c)] += 1
			except Exception as e:
				print('communityless node found')
		self.community_co_occ_mat /=2
	def create_PMIs(self):
		node_num = self.graph.number_of_nodes()
		self.PMI = np.zeros((self.community_length,self.community_length))
		for i in range(self.community_length):
			for j in range(self.community_length):
				self.PMI[i,j] = np.log((self.community_co_occ_mat[i,j]/node_num)/((self.community_co_occ_mat[i,i]/node_num)*(self.community_co_occ_mat[j,j]/node_num)))

	def create_PPMIs(self):
		self.PPMI = np.copy(self.PMI)
		self.PPMI[self.PPMI<0] = 0

	def scale_PPMIs(self):
		for i in range(self.community_length):
			self.PPMI[i,:] = self.PPMI[i,:]/np.linalg.norm(self.PPMI[i,:])

	def find_cosine_similarity(self,v1,v2):
		return (1 - spatial.distance.cosine(v1,v2))

	def find_most_similar(self,vec):
		com_keys = list(self.communities.keys())
		most_sim = None
		similarity = 0.0
		for i in range(self.community_length):
			sim = (1 - spatial.distance.cosine(vec,self.PPMI[i,:]))
			if(sim>similarity):
				similarity = sim
				most_sim = com_keys[i]
		return (most_sim,similarity)

	def get_vec(self,comm):
		com_keys = list(self.communities.keys())
		index = com_keys.index(comm)
		vec = self.PPMI[index,:]
		return vec

	def vec_plus(self,v1,v2):
		v1 = self.sanitize_vec(v1)
		v2 = self.sanitize_vec(v2)
		return v1+v2
	
	def vec_minus(self,v1,v2):
		v1 = self.sanitize_vec(v1)
		v2 = self.sanitize_vec(v2)
		return v1-v2
	
	def sanitize_vec(self,v):
		if(type(v) != np.ndarray):
			v = np.array(v)
		return v

# Testing Area
if __name__ == "__main__":
	G = nx.Graph()
	# G.add_node(1,tags= ['a','b','c'])
	# G.add_node(2,tags= ['a','c'])
	# G.add_node(3,tags= ['a','b'])
	# G.add_node(4)
	# G.add_node(5,tags = ['c','d','e'])
	# G.add_node(6,tags = ['d','e'])
	# G.add_node(7,tags = ['a','d','e'])

	G.add_node(1)
	G.add_node(2)
	G.add_node(3)
	G.add_node(4)
	G.add_node(5)
	G.add_node(6)
	G.add_node(7)

	G.add_edge(1,2)
	G.add_edge(1,3)
	G.add_edge(2,5)
	G.add_edge(1,5)
	G.add_edge(7,2)
	G.add_edge(7,3)
	G.add_edge(5,6)
	G.add_edge(5,7)
	G.add_edge(6,7)

	c = Commmunity2Vec(G)
	c.build_community_from_list([[1,2,3,7],[1,3],[1,2,5],[5,6,7]])
	# c.drop_insignificant_communities(2)
	# print(c.communities)
	c.build_community_co_occurance_matrix_edges()
	# print(c.community_co_occ_mat)
	c.create_PMIs()
	# print(c.PMI)
	c.create_PPMIs()
	# print(c.PPMI)
	c.scale_PPMIs()
	# print(c.PPMI)
	# print(c.find_cosine_similarity(c.get_vec('0'),c.get_vec('3')))
	# print(c.find_most_similar(c.vec_minus(c.get_vec('2'),c.get_vec('3'))))
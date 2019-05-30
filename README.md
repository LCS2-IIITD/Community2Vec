**Community2Vec**

This implementation contains the novel approach to embed communities as vectors as explained in the paper community2vec(http://www.aclweb.org/anthology/W17-2904). The embeddings supposed to preserve the semantic relations of the communities.

Dependencies:
- numpy
- scipy
- networkx

Idea:
Create a graph structure using networkx that contains the raw information of nodes. Using the tags present in nodes that refer the overlapping community create a matrix representation of the communities. Then create a community interaction model depending on the node overlaps or inter community edges. Embed the community info into a vector space as suggested in the referred paper.

For sample data, please visit:
http://cse.iitkgp.ac.in/resgrp/cnerg/permanence/

import networkx as nx
import dgl
import torch as th
import numpy as np
import scipy.sparse as spp

u = th.tensor([0, 0, 0, 0, 0])
v = th.tensor([1, 2, 3, 4, 5])
adj = spp.coo_matrix((np.ones(len(u)), (u.numpy(), v.numpy())))  # 稀疏矩阵
star3 = dgl.DGLGraph(adj)
nx.draw(star3.to_networkx(), with_labels=True)
plt.show()
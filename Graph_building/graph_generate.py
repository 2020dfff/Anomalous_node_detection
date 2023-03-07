import networkx as nx
# from Pre_processing import load_info
# import pandas as pd
import csv
import matplotlib.pyplot as plt

unique_edges_DST = "../data_demo/unique_edges"
unique_pairs_DST = "../data_demo/unique_pairs"
edges_input = unique_edges_DST + "/unique_edges_file.txt"
pairs_input = unique_pairs_DST + "/unique_pairs_file.txt"

# 1. read the input, unique edges
# 2. reorganize as (srcip+port, dstip+port)
# 3. generate the graph
# 4. If you want to do visualization, use number instead of address (introduce get_or_add here)

edges = []

with open(edges_input, newline='') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)  # skip header row
    for row in reader:
        src = row[1] + ':' + row[3]
        dst = row[2] + ':' + row[4]
        edges.append((src, dst))

# Print out edges list
# print(edges)

# create a new directed graph
DG = nx.DiGraph()

# build the graph with edges
for edge in edges:
    src, dst = edge
    DG.add_node(src)
    DG.add_node(dst)
    DG.add_edge(src, dst)
G = DG.to_undirected(DG)
print("graph building successful")

# basic info about the graph
is_weighted = nx.is_weighted(DG)
is_directed = nx.is_directed(DG)
print("is_weighted:", is_weighted, ", is_directed:", is_directed)

# get top 10 nodes by degree centrality
print("Top 10 nodes by degree centrality\n")
dc = nx.degree_centrality(DG)
top_nodes = sorted(dc.items(), key=lambda x: x[1], reverse=True)[:10]
for node, dc in top_nodes:
    print(f"{node}: {dc}")

# Remove nodes with degree less than x
low_degree_nodes = [node for node, degree in dict(DG.degree()).items() if degree < 300]
DG.remove_nodes_from(low_degree_nodes)

# draw the graph
nx.draw(DG, with_labels=True)
plt.savefig("path.png")
print("done")

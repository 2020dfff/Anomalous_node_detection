import networkx as nx
# from Pre_processing import load_info
# import pandas as pd
import csv
# import matplotlib.pyplot as plt

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
print(edges)

# create a new graph
G = nx.Graph()

for edge in edges:
    src, dst = edge
    G.add_node(src)
    G.add_node(dst)
    G.add_edge(src, dst)

# draw the graph
nx.draw(G, with_labels=True)


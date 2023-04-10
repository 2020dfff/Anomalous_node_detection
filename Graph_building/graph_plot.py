import csv
import os
import random
import pickle
import networkx as nx
import matplotlib.pyplot as plt

hour_dir = "../data_demo/hour_split/2022-04-07_23"
target_file = hour_dir + "/unique_edges_2022-04-07_23.txt"
reassign_target_file = hour_dir + "/reassigned_unique_edges_2022-04-07_23.txt"
abnormal_node_list = {"192.168.27.25:443", "192.168.13.187:61827", "10.3.27.91:56581", "10.3.27.215:50162"}

# Re-assign the ip with number
nmap = {}
nid = [1]


def get_or_add(n):
    if n not in nmap:
        nmap[n] = nid[0]
        nid[0] += 1
        # nid[0] += 1

    return nmap[n]


fmt_line = lambda srcip, dstip, srcport, dstport: (
        '%s,%s\n' % (
    get_or_add(srcip + ':' + srcport), get_or_add(dstip + ':' + dstport))
)

f_in = open(target_file, 'r')
f_out = open(reassign_target_file, 'w+')  # + str(cur_time) + '.txt'
line = f_in.readline()  # Skip headers
line = f_in.readline()

while line:
    tokens = line.split(',')
    reassigned_line = fmt_line(tokens[1], tokens[2], tokens[3], tokens[4])
    f_out.write(reassigned_line)
    line = f_in.readline()
f_out.close()
f_in.close()

nmap_rev = [None] * (max(nmap.values()) + 1)
for (k, v) in nmap.items():
    nmap_rev[v] = k

with open(reassign_target_file, newline='') as f:
    edges = []
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        src = row[0]
        dst = row[1]
        edges.append((src, dst))

with open(hour_dir + '/nmap.pkl', 'wb+') as f:
    pickle.dump(nmap_rev, f, protocol=pickle.HIGHEST_PROTOCOL)

# create a new directed graph
DG = nx.DiGraph()

# build the graph with edges
for edge in edges:
    src, dst = edge
    DG.add_node(src)
    DG.add_node(dst)
    DG.add_edge(src, dst)

G = DG.to_undirected(DG)
size_G = G.size(weight="weight")
print("The size of the graph is:", size_G)
components = nx.connected_components(G)  # largest connected component
largest_component = max(components, key=len)
H = G.subgraph(largest_component)
size_H = H.size(weight="weight")
print("The size of the largest subgraph is:", size_H)
print(f"graph building successful for file: {target_file}")

# randomly drop nodes
drop_fraction = 0.5
num_nodes_to_drop = int(H.number_of_nodes() * drop_fraction)
random.seed(42)
drop_nodes = random.sample(list(H.nodes()), num_nodes_to_drop)

# create a new graph without freezing it
H = H.copy()
H.remove_nodes_from(drop_nodes)

# remove edges and labels related to dropped nodes
to_remove = []
for node in drop_nodes:
    to_remove += [edge for edge in H.edges(node)]
# keep_nodes = []
# for node in H.nodes():
#     if nmap_rev[int(node)] in abnormal_node_list:
#         keep_nodes += node
to_remove += drop_nodes
H.remove_edges_from(to_remove)
# H.add_nodes_from(keep_nodes)

# Set the node color and size
pos = nx.spring_layout(H, seed=42)
node_color = ["#FF5A3E" if nmap_rev[int(node)] in abnormal_node_list else "#5DA5DA" for node in H.nodes()]
edge_color = "#444654"
nx.draw_networkx_nodes(H, pos, node_size=30, node_color=node_color)
nx.draw_networkx_edges(H, pos, width=0.5, edge_color=edge_color)
nx.draw_networkx_labels(H, pos, font_size=3, font_family="sans-serif")
plt.title('Subgraph Representation containing abnormal nodes', fontsize=12, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig(hour_dir + "/" + "graph.png", dpi=300)
plt.show()
os.remove(reassign_target_file)
os.remove(hour_dir + '/nmap.pkl')

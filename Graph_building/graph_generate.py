import networkx as nx
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from functools import partial
import csv
import matplotlib.pyplot as plt

unique_edges_DST = "../data_demo/unique_edges"
unique_pairs_DST = "../data_demo/unique_pairs"
edges_input = unique_edges_DST + "/unique_edges_file.txt"
pairs_input = unique_pairs_DST + "/unique_pairs_file.txt"
log = open(unique_pairs_DST + '/info.txt', mode='w', encoding='utf-8')

edges = []
closeness = {}

with open(pairs_input, newline='') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)  # skip header row
    for row in reader:
        src = row[1] + ':' + row[3]
        dst = row[2] + ':' + row[4]
        edges.append((src, dst))

# create a new directed graph
DG = nx.DiGraph()

# build the graph with edges
for edge in edges:
    src, dst = edge
    DG.add_node(src)
    DG.add_node(dst)
    DG.add_edge(src, dst)
G = DG.to_undirected(DG)
components = nx.connected_components(G)  # largest connected component
largest_component = max(components, key=len)
H = G.subgraph(largest_component)
print("graph building successful")


# basic info about the graph
def basic_info():
    is_weighted = nx.is_weighted(DG)
    is_directed = nx.is_directed(DG)
    print("For directed graph DG: is_weighted:", is_weighted, ", is_directed:", is_directed)
    size_DG = DG.size(weight="weight")
    print("The size of the graph is:", size_DG)
    print("===============================================")
    print("For largest subgraph H: is_connected:", nx.is_connected(H), ", is_directed:", nx.is_directed(H))
    size_H = H.size(weight="weight")
    print("The size of the graph is:", size_H)
    print("===============================================")


def compute_degree_centrality(g):
    print("Computing degree centrality...", file=log)
    dc = {}
    with tqdm(total=len(g.nodes())) as pbar:
        for node, degree in nx.degree_centrality(g).items():
            dc[node] = degree
            pbar.update(1)
    print("Top 10 nodes by degree centrality:\n")  # print top 10 nodes by degree centrality
    top_nodes = sorted(dc.items(), key=lambda x: x[1], reverse=True)[:10]
    for node, dc in top_nodes:
        print(f"{node}: {dc}", file=log)
    print("===============================================", file=log)
    return dc


def compute_betweenness_centrality(g):
    print("Computing betweenness centrality...", file=log)
    bc = {}
    with tqdm(total=len(g.nodes())) as pbar:
        for node, centrality in nx.betweenness_centrality(g, k=10, endpoints=True).items():
            bc[node] = centrality
            pbar.update(1)
    print("Top 10 nodes by betweenness centrality:\n")  # print top 10 nodes by betweenness centrality
    top_centrals = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:10]
    for node, bc in top_centrals:
        print(f"{node}: {bc}", file=log)
    print("===============================================", file=log)
    return bc


# Draw a boxplot for dc and bc
def bc_dc_boxplot(g):
    degree_values = list(nx.degree_centrality(g).values())
    betweenness_values = list(nx.betweenness_centrality(g, k=10, endpoints=True).values())
    values = [degree_values, betweenness_values]
    labels = ['Degree Centrality', 'Betweenness Centrality']
    plt.boxplot(values, labels=labels)
    plt.xlabel('Centrality Measure')
    plt.ylabel('Centrality Value')
    plt.title('Boxplot of Centrality Measures')
    plt.savefig("centrality_boxplot.png")
    plt.show()


def compute_closeness_centrality(g):
    print("Computing closeness centrality...", file=log)
    closeness = {}
    with tqdm(total=len(g.nodes())) as pbar:
        for node in g.nodes():
            closeness[node] = nx.closeness_centrality(g, u=node)
            pbar.update(1)
    return closeness


def compute_soc(g):
    print("Computing second order centrality...", file=log)
    soc = {}
    with tqdm(total=len(g.nodes())) as pbar:
        for node in g.nodes():
            soc[node] = nx.second_order_centrality(g)[node]
            pbar.update(1)
    return soc


def compute_ecc(g):
    print("Computing eccentricity...", file=log)
    ecc = {}
    with tqdm(total=len(g.nodes())) as pbar:
        for node in g.nodes():
            ecc[node] = nx.eccentricity(g, v=node)
            pbar.update(1)
    return ecc


def compute_radius_center(g):
    print("Computing radius and center...", file=log)
    with tqdm(total=2) as pbar:
        radius = nx.radius(g)
        pbar.update(1)
        center = nx.center(g)
        pbar.update(1)
    return radius, center


if __name__ == '__main__':
    # read basic info
    basic_info()
    # compute degree centrality in parallel
    compute_degree_centrality(H)
    # compute betweenness centrality in parallel
    compute_betweenness_centrality(H)
    # draw a boxplot with bc and dc
    bc_dc_boxplot(H)

    # compute closeness centrality in parallel
    with Pool(cpu_count()) as p:
        closeness = p.apply(compute_closeness_centrality, args=(H,))
    print("Top 10 nodes by closeness centrality:\n", file=log)  # print top 10 nodes by closeness centrality
    top_closes = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:10]
    for node, closeness in top_closes:
        print(f"{node}: {closeness}", file=log)
    print("===============================================", file=log)

    # compute second order centrality in parallel
    # with Pool(cpu_count()) as p:
    #     soc = p.apply(compute_soc, args=(H,))
    # print("Top 10 nodes by second order centrality:\n", file=log)  # print top 10 nodes by second order centrality
    # top_socs = sorted(soc.items(), key=lambda x: x[1], reverse=True)[:10]
    # for node, soc in top_socs:
    #     print(f"{node}: {soc}", file=log)
    # print("===============================================", file=log)

    # compute eccentricity
    # with Pool(cpu_count()) as p:
    #     ecc = p.apply(compute_ecc, args=(H,))
    # print("Top 10 nodes by eccentricity:\n", file=log)  # print top 10 nodes by second order centrality
    # top_eccs = sorted(ecc.items(), key=lambda x: x[1], reverse=True)[:10]
    # for node, ecc in top_eccs:
    #     print(f"{node}: {ecc}", file=log)
    # print("===============================================", file=log)

    # # compute radius and center
    with Pool(cpu_count()) as p:
        radius, center = p.apply(compute_radius_center, args=(H,))
    print("The radius of the graph is:", radius, file=log)
    print("The center of the graph is", center, file=log)

    # Remove nodes with degree less than x
    # low_degree_nodes = [node for node, degree in dict(DG.degree()).items() if degree < 300]
    # DG.remove_nodes_from(low_degree_nodes)
    #
    # # draw the graph
    # nx.draw(DG, with_labels=True)
    # plt.savefig("path.png")
    print("done")

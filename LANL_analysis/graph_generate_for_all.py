import os
import glob
import networkx as nx
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt

hour_dir = "../lanl_dataset/lanl_red"
log = open(hour_dir + '/info.txt', mode='w', encoding='utf-8')
abnormal_nodes = open(hour_dir + '/abnormal_nodes.txt', mode='w', encoding='utf-8')
labels_1 = open(hour_dir + '/labels_1.txt', mode='w', encoding='utf-8')

edges = []
closeness = {}
total_red_detected = 0
label_nodes = []

def process_file(file_path):
    global total_red_detected
    global label_nodes
    # Read the unique_edges file and build the graph
    edges = []

    # create a new directed graph
    G = nx.Graph()

    with open(file_path, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        # next(reader)  # skip header row
        for row in reader:
            src = row[1]  # 0
            dst = row[2]  # 1
            label = row[3]
            if label == "1":
                print(src, dst, file=labels_1)
            # build the graph with edges
            G.add_node(src, label=label)
            G.add_node(dst, label=label)
            G.add_edge(src, dst)

    # G = DG.to_undirected(DG)
    components = nx.connected_components(G)  # largest connected component
    largest_component = max(components, key=len)
    H = G.subgraph(largest_component)
    print(f"graph building successful for file: {file_path}")
    print(f"Graph features log for file: {file_path}", file=log)
    print("===============================================", file=log)

    # basic info about the graph
    def basic_info():
        is_weighted = nx.is_weighted(G)
        is_directed = nx.is_directed(G)
        print("For directed graph G: is_weighted:", is_weighted, ", is_directed:", is_directed)
        size_G = G.size(weight="weight")
        print("The size of the graph is:", size_G)
        print("===============================================")
        print("For largest subgraph H: is_connected:", nx.is_connected(H), ", is_directed:", nx.is_directed(H))
        size_H = H.size(weight="weight")
        print("The size of the graph is:", size_H)
        print("===============================================")
        # if 'label' in H.nodes[1]:
        #     print("Node 1 has a 'label' attribute:", H.nodes[1]['label'])
        # else:
        #     print("Node 1 does not have a 'label' attribute.")

    def compute_degree_centrality(g):
        red_num = 0
        print("Computing degree centrality...", file=log)
        dc = {}
        with tqdm(total=len(g.nodes())) as pbar:
            for node, degree in nx.degree_centrality(g).items():
                dc[node] = degree
                pbar.update(1)
        print("Top 20 nodes by degree centrality:\n")  # print top 20 nodes by degree centrality
        top_nodes = sorted(dc.items(), key=lambda x: x[1], reverse=True)[:20]
        for node, dc in top_nodes:
            print(f"{node}: {dc}", file=log)
            label = g.nodes[node].get('label', None)
            if label == '1':
                label_nodes.append(node)
                red_num += 1
        print("===============================================", file=log)
        return dc, red_num

    def compute_betweenness_centrality(g):
        red_num = 0
        print("Computing betweenness centrality...", file=log)
        bc = {}
        with tqdm(total=len(g.nodes())) as pbar:
            for node, centrality in nx.betweenness_centrality(g, k=10, endpoints=True).items():
                bc[node] = centrality
                pbar.update(1)
        print("Top 20 nodes by betweenness centrality:\n")  # print top 20 nodes by betweenness centrality
        top_centrals = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:20]
        for node, bc in top_centrals:
            print(f"{node}: {bc}", file=log)
            label = g.nodes[node].get('label', None)
            if label == '1':
                label_nodes.append(node)
                red_num += 1
        print("===============================================", file=log)
        return bc, red_num

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
        # filename = os.path.basename(file_path).split("_")[3]  # [:-3]
        # plt.savefig(hour_dir + "/" + filename + "_centrality_boxplot.png")
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
        red_num = 0
        print("Computing radius and center...", file=log)
        with tqdm(total=1) as pbar:
            # radius = nx.radius(g)
            # pbar.update(1)
            center = nx.center(g)
            for node in center:
                center_labels = g.nodes[node].get('label', None)
                if center_labels == '1':
                    label_nodes.append(node)
                    red_num += 1
            # # get the labels of the center nodes
            # center_labels = {node: g.nodes[node].get('label', None) for node in center}
            # center_label_count = sum(1 for label in center_labels.values() if label == '1')  # count the number
            pbar.update(1)
        return center, red_num  # radius

    # read basic info
    basic_info()
    # compute degree centrality in parallel
    _, red_num = compute_degree_centrality(H)
    total_red_detected += red_num
    # compute betweenness centrality in parallel
    _, red_num = compute_betweenness_centrality(H)
    total_red_detected += red_num
    # draw a boxplot with bc and dc
    # bc_dc_boxplot(H)

    # compute closeness centrality in parallel
    closeness = compute_closeness_centrality(H)
    print("Top 20 nodes by closeness centrality:\n", file=log)  # print top 20 nodes by closeness centrality
    top_closes = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:20]
    for node, closeness in top_closes:
        print(f"{node}: {closeness}", file=log)
        label = H.nodes[node].get('label', None)
        if label == '1':
            label_nodes.append(node)
            total_red_detected += 1
    print("===============================================", file=log)

    # compute second order centrality in parallel
    # soc = compute_soc(H)
    # print("Top 20 nodes by second order centrality:\n", file=log)  # print top 20 nodes by second order centrality
    # top_socs = sorted(soc.items(), key=lambda x: x[1], reverse=True)[:20]
    # for node, soc in top_socs:
    #     print(f"{node}: {soc}", file=log)
    # print("===============================================", file=log)

    # compute eccentricity
    ecc = compute_ecc(H)
    print("Top 20 nodes by eccentricity:\n", file=log)  # print top 20 nodes by second order centrality
    top_eccs = sorted(ecc.items(), key=lambda x: x[1], reverse=True)[:20]
    for node, ecc in top_eccs:
        print(f"{node}: {ecc}", file=log)
        label = H.nodes[node].get('label', None)
        if label == '1':
            label_nodes.append(node)
            total_red_detected += 1
    print("===============================================", file=log)

    # # compute radius and center
    center, center_label_count = compute_radius_center(H)  # radius, center, center_label_count
    total_red_detected += center_label_count
    # print("The radius of the graph is:", radius, file=log)
    print("The center of the graph is", center, file=log)

    # Remove nodes with degree less than x
    # low_degree_nodes = [node for node, degree in dict(DG.degree()).items() if degree < 300]
    # DG.remove_nodes_from(low_degree_nodes)
    #
    # # draw the graph
    # nx.draw(DG, with_labels=True)
    # plt.savefig("path.png")
    print("Now the total number of red_events detected is:", total_red_detected)
    print("And the list of abnormal nodes:", label_nodes)
    print("done")


if __name__ == '__main__':
    # file_list = glob.glob(os.path.join(hour_dir, '*.txt'))
    # for file_path in file_list:
    #     process_file(file_path)
    for subdir, dirs, files in os.walk(hour_dir):
        for file in files:
            if file.startswith("auth_"):
                file_path = os.path.join(subdir, file)
                process_file(file_path)

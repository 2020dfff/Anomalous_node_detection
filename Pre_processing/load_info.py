"""
    Created on: 2023-01-10
    Author: Yang Fei
"""

import os
import json
import pickle
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
# from tqdm import tqdm

DST = "../data_demo"

input_file = DST + "/input.txt"
abnormal_file = DST + "/without_port.txt"
unique_edges_file = DST + "/unique_edges/unique_edges_file.txt"
unique_pairs_file = DST + "/unique_pairs/unique_pairs_file.txt"  # re-organize the file, also make edge unique
reassign_edges_file = DST + "/unique_edges/reassigned_edges.txt"
reassign_pairs_file = DST + "/unique_pairs/reassigned_pairs.txt"  # give the ip address new number
log = open(DST + '/info.txt', mode='w', encoding='utf-8')


def preprocess(infile, outfile1, outfile2, origin_out):
    # delete the blank line in the dataset to guarantee the function works
    edges = set()
    pairs = set()
    with open(infile, "r") as file:
        lines = file.readlines()
    lines = [line for line in lines if line.strip()]
    with open(outfile1, "w") as f_edge_out, \
            open(outfile2, "w") as f_pair_out, \
            open(origin_out, "w") as origin_data_out:
        f_edge_out.write("proto_name,srcip,dstip,srcport,dstport\n")
        f_pair_out.write("proto_name,srcip,dstip,srcport,dstport\n")

        # extract edges and pairs from the data
        for line in lines:
            json_line = json.loads(f"{line}\n")

            proto_name = json_line.get("_source", {}).get("proto_name", "")
            srcip = json_line.get("_source", {}).get("srcip", "")
            dstip = json_line.get("_source", {}).get("dstip", "")
            srcport = json_line.get("_source", {}).get("srcport", "")
            dstport = json_line.get("_source", {}).get("dstport", "")

            if (srcport == "") or (dstport == ""):
                origin_data_out.write(line)

            # add unique edges and pairs to sets
            edge = (srcip, dstip, srcport, dstport)
            pair = (srcip, dstip)
            if edge not in edges:
                f_edge_out.write(f"{proto_name},{srcip},{dstip},{srcport},{dstport}\n")
                edges.add(edge)

            if pair not in pairs:
                f_pair_out.write(f"{proto_name},{srcip},{dstip},{srcport},{dstport}\n")
                pairs.add(pair)

    return edges, pairs


def split():
    # do the initialization job to pick out key information
    if not os.path.exists(DST + "/unique_edges"):
        os.makedirs(DST + "/unique_edges")
    if not os.path.exists(DST + "/unique_pairs"):
        os.makedirs(DST + "/unique_pairs")
    preprocess(input_file, unique_edges_file, unique_pairs_file, abnormal_file)

    # Re-assign the ip with number
    nmap = {}
    nid = [1]

    def get_or_add(n):
        if n not in nmap:
            nmap[n] = nid[0]
            nid[0] += 1
            # nid[0] += 1

        return nmap[n]

    fmt_line = lambda proto, srcip, dstip, srcport, dstport: (
            '%s,%s,%s,%s,%s' % (
        proto, get_or_add(srcip), get_or_add(dstip), srcport, dstport))

    f_in1 = open(unique_pairs_file, 'r')
    f_out1 = open(reassign_pairs_file, 'w+')  # + str(cur_time) + '.txt'
    line = f_in1.readline()  # Skip headers
    line = f_in1.readline()

    while line:
        tokens = line.split(',')
        reassigned_line = fmt_line(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])
        f_out1.write(reassigned_line)
        line = f_in1.readline()
    f_out1.close()
    f_in1.close()

    f_in2 = open(unique_edges_file, 'r')
    f_out2 = open(reassign_edges_file, 'w+')
    line = f_in2.readline()  # Skip headers
    line = f_in2.readline()

    while line:
        tokens = line.split(',')
        reassigned_line = fmt_line(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])
        f_out2.write(reassigned_line)
        line = f_in2.readline()
    f_out2.close()
    f_in2.close()

    nmap_rev = [None] * (max(nmap.values()) + 1)
    for (k, v) in nmap.items():
        nmap_rev[v] = k

    with open(DST + '/nmap.pkl', 'wb+') as f:
        pickle.dump(nmap_rev, f, protocol=pickle.HIGHEST_PROTOCOL)
    # print(nmap_rev[3])  # output: 10.3.27.203

    print("For unique pairs:\n", file=log)
    calculate(reassign_pairs_file, nmap_rev)
    print("***************************************************************************************************\n",
          file=log)
    print("For unique edges:\n", file=log)
    calculate(reassign_edges_file, nmap_rev)


# Calculate some key information about the data
def calculate(target_file, nmap_rev):
    df = pd.read_csv(target_file, header=None)
    # Basic information about the file
    print("The name of this file is: %s\n=====================================================================" % str(
        target_file), file=log)
    total_edge = 0
    total_node = 0
    edge_without_src_port = 0
    edge_without_dst_port = 0
    edge_without_port = 0
    with open(target_file, 'r') as tmp:
        for edge in tmp:
            total_edge += 1
            columns = edge.split(',')
            if len(columns) >= 3:
                number_2 = int(columns[1])
                number_3 = int(columns[2])
                if number_2 > total_node:
                    total_node = number_2
                if number_3 > total_node:
                    total_node = number_3
                if columns[3] == "":
                    edge_without_src_port += 1
                if columns[4] == "\n":
                    edge_without_dst_port += 1
                if (columns[3] == "") or (columns[4] == '\n'):
                    edge_without_port += 1
    print(
        "Total number of edges: %s\n=====================================================================" % total_edge,
        file=log)
    print(
        "Total number of nodes: %s\n=====================================================================" % total_node,
        file=log)
    total_port = len(set(df[3].tolist() + df[4].tolist()))
    print(
        "Total number of ports: %s\n=====================================================================" % total_port,
        file=log)
    normal_percent = (1 - edge_without_port / total_edge) * 100
    print("edge_without_src_port: %s, edge_without_dst_port: %s, edge_without_port: %s\n"
          "=====================================================================" % (edge_without_src_port,
                                                                                     edge_without_dst_port,
                                                                                     edge_without_port), file=log)
    print(
        'Normal edges percent: %f%%\n=====================================================================' % normal_percent,
        file=log)

    # calculate the Node egress and ingress
    counts_in = df[1].value_counts()
    counts_out = df[2].value_counts()

    # Print the top 10 node with the highest ingress
    top_in_nodes = counts_in.head(10).index.tolist()
    top_in_ip = [nmap_rev[node] for node in top_in_nodes]
    print("The top ten IPs with the largest ingress:\n", top_in_ip, file=log)
    print("=====================================================================", file=log)

    # Print the top 10 node with the highest egress
    top_out_nodes = counts_out.head(10).index.tolist()
    top_out_ip = [nmap_rev[node] for node in top_out_nodes]
    print("The top ten IPs with the largest egress:\n", top_out_ip, file=log)
    print("=====================================================================", file=log)
    print("done!")

    # check whether the abnormal ports origin from one or multiple fixed nodes
    missing_rows = df[df[3].isnull() | df[4].isnull()]
    key_nodes = missing_rows[1].unique()
    counts = missing_rows[1].value_counts()

    if len(key_nodes) == 1:
        print(f"Abnormal ports generate from a single unique ip\n: {nmap_rev[key_nodes[0]]}", file=log)
    else:
        key_ips = [nmap_rev[node] for node in key_nodes]
        print("Abnormal ports generate from multiple unique ips:\n", key_ips, file=log)

        # Plot the wordcloud of key_ips results in abnormal ports
        ip_addresses = [nmap_rev[node] for node in counts.index.tolist()]
        ip_counts = counts.values.tolist()
        print(list(zip(ip_addresses, ip_counts)))
        wc = WordCloud(background_color=None, mode='RGBA', max_words=100, width=400, height=400, min_font_size=5,
                       max_font_size=150,
                       collocations=False, scale=20, margin=2, prefer_horizontal=1, mask=np.array(Image.open('1.png')))
        ip_count_dict = dict(zip(ip_addresses, ip_counts))
        wc.generate_from_frequencies(ip_count_dict)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        wc.to_file(DST + '/' + str(os.path.splitext(target_file)[0]) + "_wordcloud.png")
        plt.show()

    # Plot and show the boxplot in each situation
    data = [counts_in.values, counts_out.values]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(data)
    ax.set_xlabel('Data Type')
    ax.set_ylabel('Number of Packets')
    ax.set_xticklabels(['Ingress', 'Egress'])
    plt.show()
    fig.savefig(DST + '/' + str(os.path.splitext(target_file)[0]) + "_boxplot.png")


if __name__ == '__main__':
    split()
    log.close()

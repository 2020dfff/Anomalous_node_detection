"""
    Created on: 2023-01-10
    Author: Yang Fei
"""

import os
import json
import pickle
import pandas as pd

# from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
# from tqdm import tqdm

DST = "../data_demo"

input_file = DST + "/input.txt"
modified_file = DST + "/modified.txt"  # delete blank line
output_file = DST + "/output.txt"  # re-organize the file
reassign_file = DST + "/reassigned.txt"  # give the ip address new number


# delete the blank line in the dataset to guarantee the function works
def delete_blank_line(infile, modified):
    with open(infile, "r") as file:
        lines = file.readlines()

    with open(modified, "w+") as file:
        for line in lines:
            if line.strip():
                file.write(line)


def json_keyword():
    delete_blank_line(input_file, modified_file)
    with open(modified_file, "r") as f_in, open(output_file, "w+") as f_out:
        f_out.write("proto_name,srcip,dstip,srcport,dstport\n")
        for line in f_in:
            json_line = json.loads(line)

            proto_name = json_line.get("_source", {}).get("proto_name", "")
            srcip = json_line.get("_source", {}).get("srcip", "")
            dstip = json_line.get("_source", {}).get("dstip", "")
            srcport = json_line.get("_source", {}).get("srcport", "")
            dstport = json_line.get("_source", {}).get("dstport", "")

            f_out.write(f"{proto_name},{srcip},{dstip},{srcport},{dstport}\n")


def split():
    # do the initialization job to pick out key information
    json_keyword()

    # Re-assign the ip with number
    f_in = open(output_file, 'r')
    f_out = open(reassign_file, 'w+')  # + str(cur_time) + '.txt'

    line = f_in.readline()  # Skip headers
    line = f_in.readline()

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

    while line:
        tokens = line.split(',')
        reassigned_line = fmt_line(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])

        f_out.write(reassigned_line)
        line = f_in.readline()

    f_out.close()
    f_in.close()

    nmap_rev = [None] * (max(nmap.values()) + 1)
    for (k, v) in nmap.items():
        nmap_rev[v] = k

    with open(DST + '/nmap.pkl', 'wb+') as f:
        pickle.dump(nmap_rev, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Calculate some key information about the data
    def calculate(target_file):
        df = pd.read_csv(target_file, header=None)
        # Basic information about the file
        print("The name of this file is:", str(target_file))
        print("=====================================================================")
        total_edge = 0
        total_node = 0
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
                    if (columns[3] == "") or (columns[4] == ""):
                        edge_without_port += 1
        print("Total number of edges:", total_edge)
        print("Total number of nodes:", total_node)
        total_port = len(set(df[3].tolist() + df[4].tolist()))
        print("Total number of ports:", total_port)
        print("=====================================================================")
        normal_percent = (1-edge_without_port/total_edge)*100
        print('Normal edges percent: %f%%:' % normal_percent)
        print("=====================================================================")

        # calculate the Node egress and ingress
        counts_in = df[1].value_counts()
        counts_out = df[2].value_counts()

        # Print the top 10 node with the highest ingress
        top_in_nodes = counts_in.head(10).index.tolist()
        top_in_ip = [nmap_rev[node] for node in top_in_nodes]
        print("The top ten IPs with the largest ingress:\n", top_in_ip)
        print("=====================================================================")

        # Print the top 10 node with the highest egress
        top_out_nodes = counts_out.head(10).index.tolist()
        top_out_ip = [nmap_rev[node] for node in top_out_nodes]
        print("The top ten IPs with the largest egress:\n", top_out_ip)
        print("=====================================================================")

    calculate(reassign_file)


if __name__ == '__main__':
    split()

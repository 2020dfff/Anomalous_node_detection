import os
import json

DST = "../data_demo/abnormal_raw_data"
input_file = "../data_demo/input.txt"
top_srcport_file = DST + "/top_srcport.txt"
top_dstport_file = DST + "/top_dstport.txt"
abnormal_node_file = DST + "/abnormal_graph_features.txt"
abnormal_node_file2 = DST + "/abnormal_graph_features_2.txt"

def get_raw_0(infile, origin_out):
    # delete the blank line in the dataset to guarantee the function works
    with open(infile, "r") as file:
        lines = file.readlines()
    lines = [line for line in lines if line.strip()]
    with open(origin_out, "w") as origin_data_out:
        # extract edges and pairs from the data
        for line in lines:
            json_line = json.loads(f"{line}\n")
            proto_name = json_line.get("_source", {}).get("proto_name", "")
            srcip = json_line.get("_source", {}).get("srcip", "")
            dstip = json_line.get("_source", {}).get("dstip", "")
            srcport = json_line.get("_source", {}).get("srcport", "")
            dstport = json_line.get("_source", {}).get("dstport", "")

            if (srcip == "192.168.27.25") and (dstip == "10.3.27.233" or dstip == "10.3.27.66" or dstip == "10.3.27.34" or dstip == "10.3.27.103" or dstip == "10.3.27.208"):
                origin_data_out.write(line)


def get_raw_1(infile, origin_out):
    # delete the blank line in the dataset to guarantee the function works
    with open(infile, "r") as file:
        lines = file.readlines()
    lines = [line for line in lines if line.strip()]
    with open(origin_out, "w") as origin_data_out:
        # extract edges and pairs from the data
        for line in lines:
            json_line = json.loads(f"{line}\n")
            proto_name = json_line.get("_source", {}).get("proto_name", "")
            srcip = json_line.get("_source", {}).get("srcip", "")
            dstip = json_line.get("_source", {}).get("dstip", "")
            srcport = json_line.get("_source", {}).get("srcport", "")
            dstport = json_line.get("_source", {}).get("dstport", "")

            if (srcip == "10.3.27.233") and (dstip == "192.168.27.25"):
                origin_data_out.write(line)


def get_raw_2(infile, origin_out):
    # delete the blank line in the dataset to guarantee the function works
    with open(infile, "r") as file:
        lines = file.readlines()
    lines = [line for line in lines if line.strip()]
    with open(origin_out, "w") as origin_data_out:
        # extract edges and pairs from the data
        for line in lines:
            json_line = json.loads(f"{line}\n")
            proto_name = json_line.get("_source", {}).get("proto_name", "")
            srcip = json_line.get("_source", {}).get("srcip", "")
            dstip = json_line.get("_source", {}).get("dstip", "")
            srcport = json_line.get("_source", {}).get("srcport", "")
            dstport = json_line.get("_source", {}).get("dstport", "")

            if ((srcip == "192.168.27.15") and (srcport == 53))\
                    or ((srcip == "192.168.27.8") and (srcport == 53))\
                        or ((srcip == "192.168.27.25") and (srcport == 443)):
                origin_data_out.write(line)


def get_raw_3(infile, origin_out):
    # delete the blank line in the dataset to guarantee the function works
    with open(infile, "r") as file:
        lines = file.readlines()
    lines = [line for line in lines if line.strip()]
    with open(origin_out, "w") as origin_data_out:
        # extract edges and pairs from the data
        for line in lines:
            json_line = json.loads(f"{line}\n")
            proto_name = json_line.get("_source", {}).get("proto_name", "")
            srcip = json_line.get("_source", {}).get("srcip", "")
            dstip = json_line.get("_source", {}).get("dstip", "")
            srcport = json_line.get("_source", {}).get("srcport", "")
            dstport = json_line.get("_source", {}).get("dstport", "")

            if ((srcip == "192.168.112.185") and (srcport == 55383))\
                    or ((srcip == "192.168.112.39") and (srcport == 58304))\
                        or ((srcip == "192.168.112.189") and (srcport == 50757)):
                origin_data_out.write(line)


get_raw_0(input_file, top_dstport_file)  # top srcport node
# get_raw_1(input_file, top_srcport_file)  # top srcport node
# get_raw_2(input_file, abnormal_node_file)  # abnormal graph features node
# get_raw_3(input_file, abnormal_node_file2)  # abnormal graph features node, with dynamic/private port

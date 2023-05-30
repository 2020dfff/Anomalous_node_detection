import os
import json

DST = "../done_dataset/0212/abnormal_raw_data"
input_file = "../done_dataset/0212/2022-02-12(1644624000000)~2022-02-13(1644710400000)-aella-adr.txt"
# top_srcport_file = DST + "/top_srcport.txt"
# top_dstport_file = DST + "/top_dstport.txt"
abnormal_node_file1 = DST + "/4.2.2.2_53.txt"
abnormal_node_file2 = DST + "/3.92.7.89_8888.txt"
abnormal_node_file3 = DST + "/10.1.28.3.txt"
abnormal_node_file4 = DST + "/10.255.1.7.txt"
abnormal_node_file5 = DST + "/209.244.0.3_53.txt"
abnormal_node_file6 = DST + "/10.1.10.253_53.txt"
abnormal_node_file7 = DST + "/10.47.3.91_54535.txt"
abnormal_node_file8 = DST + "/10.12.4.11_47001.txt"
abnormal_node_file9 = DST + "/10.1.10.251_53.txt"
abnormal_node_file10 = DST + "/54.158.67.192_9997.txt"
abnormal_node_file11 = DST + "/18.233.248.145_9997.txt"
abnormal_node_file12 = DST + "/204.186.31.193.txt"


def get_raw_1(infile, origin_out, src_ip, src_port):
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

            if (srcip == src_ip) and (srcport == src_port):
                origin_data_out.write(line)


def get_raw_2(infile, origin_out, src_ip):
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

            if (srcip == src_ip):
                origin_data_out.write(line)


# 02.13
# get_raw_1(input_file, abnormal_node_file1, src_ip="4.2.2.2", src_port=53)
# get_raw_1(input_file, abnormal_node_file2, src_ip="3.92.7.89", src_port=8888)
# get_raw_2(input_file, abnormal_node_file3, src_ip="10.1.28.3")
# get_raw_2(input_file, abnormal_node_file4, src_ip="10.255.1.7")
# get_raw_1(input_file, abnormal_node_file5, src_ip="209.244.0.3", src_port=53)
# get_raw_1(input_file, abnormal_node_file6, src_ip="10.1.10.253", src_port=53)
# get_raw_1(input_file, abnormal_node_file7, src_ip="10.47.3.91", src_port=54535)
# get_raw_1(input_file, abnormal_node_file8, src_ip="10.12.4.11", src_port=47001)

# 02.12
# get_raw_1(input_file, abnormal_node_file9, src_ip="10.1.10.251", src_port=53)
# get_raw_1(input_file, abnormal_node_file10, src_ip="54.158.67.192", src_port=9997)
# get_raw_1(input_file, abnormal_node_file11, src_ip="18.233.248.145", src_port=9997)
get_raw_2(input_file, abnormal_node_file12, src_ip="204.186.31.193")

# 4.2.2.2:53/3.92.7.89:8888/10.1.28.3:xxx/10.255.1.7:xxxx/209.244.0.3:53/10.1.10.253:53/10.47.3.91:54535/10.12.4.11:47001
# dc,bc,cc.center/same(-center)/all cc/4-6,9-13, all/dc bc cc/dc bc cc, center/dc, cc, center/14:dc,bc

# 10.1.10.251:53/54.158.67.192:9997/18.233.248.145:9997/204.186.31.193:xxx
# dc, bc/dc/dc/center

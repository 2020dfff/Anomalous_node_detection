import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

DST = "../done_dataset/0212"
input_file = DST + "/2022-02-12(1644624000000)~2022-02-13(1644710400000)-aella-adr.txt"
hour_split = DST + "/hour_split"


# def preprocess(infile, outdir):
#     # Create output directory if it doesn't exist
#     if not os.path.exists(outdir):
#         os.makedirs(outdir)
#
#     # Extract edges and pairs from the data, and write to hourly files
#     edge_files = {}
#     pair_files = {}
#     records_per_hour = {}
#     with open(infile, "r") as f:
#         # Delete blank lines from input file
#         lines = f.readlines()
#         lines = [line for line in lines if line.strip()]
#
#         for line in lines:
#             json_line = json.loads(line)
#             timestamp = int(json_line["_source"]["timestamp"]) // 1000  # Convert to seconds
#
#             # Get hour from timestamp
#             hour = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d_%H')
#
#             # Create directory for this hour if it doesn't exist
#             hour_dir = os.path.join(outdir, hour)
#             if not os.path.exists(hour_dir):
#                 os.makedirs(hour_dir)
#
#             # Extract edge and pair information
#             proto_name = json_line.get("_source", {}).get("proto_name", "")
#             srcip = json_line.get("_source", {}).get("srcip", "")
#             dstip = json_line.get("_source", {}).get("dstip", "")
#             srcport = json_line.get("_source", {}).get("srcport", "")
#             dstport = json_line.get("_source", {}).get("dstport", "")
#
#             # Get or create file handles and edge/pair sets for this hour
#             if hour not in edge_files:
#                 edge_files[hour] = open(os.path.join(hour_dir, f"unique_edges_{hour}.txt"), "w")
#                 edge_files[hour].write("proto_name,srcip,dstip,srcport,dstport\n")
#                 edge_files[hour].edges_seen = set()
#             if hour not in pair_files:
#                 pair_files[hour] = open(os.path.join(hour_dir, f"unique_pairs_{hour}.txt"), "w")
#                 pair_files[hour].write("proto_name,srcip,dstip,srcport,dstport\n")
#                 pair_files[hour].pairs_seen = set()
#
#             # Write unique edges and pairs to files
#             edge = (srcip, dstip, srcport, dstport)
#             pair = (srcip, dstip)
#             if edge not in edge_files[hour].edges_seen:
#                 edge_files[hour].write(f"{proto_name},{srcip},{dstip},{srcport},{dstport}\n")
#                 edge_files[hour].edges_seen.add(edge)
#             if pair not in pair_files[hour].pairs_seen:
#                 pair_files[hour].write(f"{proto_name},{srcip},{dstip},{srcport},{dstport}\n")
#                 pair_files[hour].pairs_seen.add(pair)
#
#             # Count the number of records in each hour
#             if hour not in records_per_hour:
#                 records_per_hour[hour] = 0
#             records_per_hour[hour] += 1
#
#     # Close file handles
#     for f in edge_files.values():
#         f.close()
#     for f in pair_files.values():
#         f.close()
#
#     # Draw a histogram of the number of records in each hour
#     hours = list(records_per_hour.keys())
#     hours.sort()
#     counts = [records_per_hour[hour] for hour in hours]
#     fig, ax = plt.subplots()


def plot_process(infile):
    # Count number of records per hour
    records_per_hour = {}
    with open(infile, "r") as f:
        lines = f.readlines()
        lines = [line for line in lines if line.strip()]

        for line in lines:
            json_line = json.loads(line)
            timestamp = int(json_line["_source"]["timestamp"]) // 1000  # Convert to seconds
            hour = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d_%H')
            if hour not in records_per_hour:
                records_per_hour[hour] = 0
            records_per_hour[hour] += 1

    # Plot histogram
    hours = sorted(records_per_hour.keys())
    values = [records_per_hour[h] for h in hours]
    plt.bar(hours, values)
    plt.xticks(rotation=90)
    plt.xlabel("Hour")
    plt.ylabel("Number of records")
    plt.title("Number of records per hour")
    plt.savefig(hour_split + "/" + "time_distribute.png", dpi=300)
    plt.show()


plot_process(input_file)

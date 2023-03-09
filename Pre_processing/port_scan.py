import json
from collections import defaultdict

# Set the path to the JSON-like text file
DST = "../data_demo"
input_file = DST + "/input.txt"

# Define dictionaries to store the IP counts for each port
srcport_ip_counts = defaultdict(set)
dstport_ip_counts = defaultdict(set)

# Read the JSON-like text file and iterate over the lines
with open(input_file) as f:
    for line in f:
        try:
            flow = json.loads(line.strip())
        except json.JSONDecodeError:
            continue  # skip lines that are not valid JSON
        src_port = flow.get("_source", {}).get("srcport", None)
        dst_port = flow.get("_source", {}).get("dstport", None)
        src_ip = flow.get("_source", {}).get("srcip", None)
        dst_ip = flow.get("_source", {}).get("dstip", None)
        if src_port and src_ip:
            srcport_ip_counts[src_port].add(src_ip)
        if dst_port and dst_ip:
            dstport_ip_counts[dst_port].add(dst_ip)

# Print the IP counts for each port in the order of increasing number of unique IPs
print("Unique source IPs for each source port:")
for port, ip_set in sorted(srcport_ip_counts.items(), key=lambda x: len(x[1])):
    print(f"Source port {port} has {len(ip_set)} unique source IPs.")

print("\nUnique destination IPs for each destination port:")
for port, ip_set in sorted(dstport_ip_counts.items(), key=lambda x: len(x[1])):
    print(f"Destination port {port} has {len(ip_set)} unique destination IPs.")

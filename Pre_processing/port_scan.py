import json
from collections import defaultdict
import matplotlib.pyplot as plt

DST = "../data_demo"
input_file = DST + "/input.txt"
results = defaultdict(set)

# Open the text file and read the data
with open(input_file, 'r') as file:
    for record in file:
        try:
            flow = json.loads(record.strip())
        except json.JSONDecodeError:
            continue  # skip lines that are not valid JSON
        src_port = flow.get("_source", {}).get("srcport", None)
        dst_port = flow.get("_source", {}).get("dstport", None)
        src_ip = flow.get("_source", {}).get("srcip", None)
        dst_ip = flow.get("_source", {}).get("dstip", None)

        key = (src_ip, dst_ip)
        value = src_port

        results[key].add(value)

for key, values in sorted(results.items(), key=lambda item: len(item[1]), reverse=True):
    print(key, len(values))

# Get the lengths of the values sets
# lengths = [len(values) for values in results.values()]
# fig, ax = plt.subplots()
# ax.boxplot(lengths)
# ax.set_ylabel('Length of values')
# plt.show()
# fig.savefig(DST + '/' + "_portscan_boxplot.png")
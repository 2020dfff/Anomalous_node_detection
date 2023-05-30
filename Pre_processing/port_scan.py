import json
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

DST = "../1/aella-adr-abnormal"
input_file = DST + "/2022-02-13(1644710400000)~2022-02-14(1644796800000)-aella-adr.txt"
src_results = defaultdict(set)
dst_results = defaultdict(set)

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
        src_value = src_port
        dst_value = dst_port

        src_results[key].add(src_value)
        dst_results[key].add(dst_value)

print("top 10 srcport\n")
top_src_10 = sorted(src_results.items(), key=lambda item: len(item[1]), reverse=True)[:10]
for key, values in top_src_10:
    print(key, len(values))

print("Now top 10 dstport\n")
top_dst_10 = sorted(dst_results.items(), key=lambda item: len(item[1]), reverse=True)[:10]
for key, values in top_dst_10:
    print(key, len(values))

# Get the lengths of the values sets
lengths_src = [len(values) for values in src_results.values()]
lengths_dst = [len(values) for values in dst_results.values()]

# Plot a boxplot to show the distribution of the data
data = [lengths_src, lengths_dst]
fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(data)
ax.set_xlabel('Data Type')
ax.set_ylabel('Length of values')
ax.set_xticklabels(['srcport', 'dstport'])
plt.show()
fig.savefig(DST + '/port_scan_fig' + "/portscan_boxplot.png")

# # Plot a violin plot to show the distribution of the data
# fig, ax = plt.subplots()
# sns.violinplot(y=lengths_src, ax=ax)
# ax.set_ylabel('Length of values')
# ax.set_title('Distribution of length of values')
# plt.show()
# fig.savefig(DST + '/port_scan_fig' + "/portscan_violinplot.png")
#
# # Plot a scatter plot to show the distribution of the data
# fig, ax = plt.subplots()
# ax.scatter(range(len(lengths_src)), lengths_src)
# ax.set_ylabel('Length of values')
# ax.set_title('Distribution of length of values')
# plt.show()
# fig.savefig(DST + '/port_scan_fig' + "/portscan_scatterplot.png")


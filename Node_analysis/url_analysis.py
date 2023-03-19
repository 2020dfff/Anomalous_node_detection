import json

DST = "../data_demo/abnormal_raw_data"
input_file = "../data_demo/input.txt"
top_dstport_file = DST + "/top_dstport.txt"
abnormal_node_file = DST + "/abnormal_graph_features.txt"

# Load JSON data from file
urls = {}
with open(abnormal_node_file, 'r') as f:
    data = f.readlines()

    # Iterate over JSON objects in file
    for line in data:
        # Parse JSON object
        obj = json.loads(line.strip())
        # Extract request URL from object
        request_url = obj['_source']['request_url']
        # Increment count for URL in dictionary
        if request_url in urls:
            urls[request_url] += 1
        else:
            urls[request_url] = 1

# Print out counts for each URL
for url, count in urls.items():
    print(f"{url}: {count}")

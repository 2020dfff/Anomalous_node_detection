import json

DST = "../done_dataset/0213/abnormal_raw_data"
input_file = "../1/aella-adr-abnormal/2022-02-13(1644710400000)~2022-02-14(1644796800000)-aella-adr.txt"
top_dstport_file = DST + "/top_dstport.txt"
abnormal_node_file = DST + "/abnormal_graph_features.txt"

# Load JSON data from file
urls = {}
with open(top_dstport_file, 'r') as f:
    data = f.readlines()
    lines = [line for line in data if line.strip()]

    # Iterate over JSON objects in file
    for line in lines:
        # Parse JSON object
        obj = json.loads(line.strip())
        # Extract request URL from object
        request_url = obj.get("_source", {}).get("request_url", "")
        # request_url = obj['_source']['request_url']
        # Increment count for URL in dictionary
        if request_url in urls:
            urls[request_url] += 1
        else:
            urls[request_url] = 1

# Print out counts for each URL
for url, count in urls.items():
    # urls = sorted(urls.items(), key=lambda x: x[1], reverse=True)
    # print(urls)
    print(f"{url}: {count}")

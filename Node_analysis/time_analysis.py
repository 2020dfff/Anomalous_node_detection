import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

DST = "../1/aella-adr-abnormal/abnormal_raw_data"
input_file = "../data_demo/input.txt"
top_dstport_file = DST + "/top_dstport.txt"
abnormal_node_file = DST + "/abnormal_graph_features.txt"

# Load JSON data from file
timestamps = []
dstports = []
with open(top_dstport_file, 'r') as f:
    data = f.readlines()

    # Iterate over JSON objects in file
    for line in data:
        # Parse JSON object
        obj = json.loads(line.strip())
        # Extract timestamp from object
        timestamp = obj['_source']['timestamp']
        # Convert Unix timestamp to datetime object
        dt = datetime.fromtimestamp(timestamp/1000)
        # Add datetime object to list
        timestamps.append(dt)
        # Extract dstport from object
        dstport = obj['_source']['dstport']
        # Add dstport to list
        dstports.append(dstport)

# Define time range
start_time = min(timestamps)
end_time = max(timestamps)
delta = timedelta(hours=1)
time_range = []
while start_time <= end_time:
    time_range.append(start_time)
    start_time += delta

# Count timestamps and unique dstports for each hour
timestamps_per_hour = []
unique_dstports_per_hour = []
for hour_start in time_range:
    hour_end = hour_start + delta
    timestamps_in_hour = len([t for t in timestamps if hour_start <= t < hour_end])
    timestamps_per_hour.append(timestamps_in_hour)
    dstports_in_hour = len(set([dstports[i] for i in range(len(dstports)) if hour_start <= timestamps[i] < hour_end]))
    unique_dstports_per_hour.append(dstports_in_hour)
    print(f"{hour_start} - {hour_end}: {timestamps_in_hour} timestamps, {dstports_in_hour} unique dstports")

# # Plot results
# fig, ax1 = plt.subplots()
# ax1.plot(time_range, timestamps_per_hour, color='blue')
# ax1.set_xlabel('Time')
# ax1.set_ylabel('Number of timestamps', color='blue')
# ax1.tick_params(axis='y', labelcolor='blue')
#
# ax2 = ax1.twinx()
# ax2.plot(time_range, unique_dstports_per_hour, color='red')
# ax2.set_ylabel('Number of unique dstports', color='red')
# ax2.tick_params(axis='y', labelcolor='red')
#
# plt.title('Timestamps and unique dstports per hour')
# plt.show()

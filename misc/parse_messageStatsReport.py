import os
import csv
import argparse
import fnmatch

parser = argparse.ArgumentParser(description='Parse selected .txt files in a directory.')
parser.add_argument('--input', type=str, help='the path to the directory')
parser.add_argument('--output', type=str, help='the path to the directory where the result .csv is saved')
args = parser.parse_args()

pattern="*MessageStatsReport.txt"

def extract_values_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    values = {}
    for line in lines:
        if ':' in line:
            key, value = line.strip().split(': ')
            try:
                value = float(value)
            except ValueError:
                pass
            values[key] = value

    return values

output = [["sep=,"],["RoutingAlgorithm","Scenario","MovementModel","BucketPolicy","SendPolicy","DropPolicy","Nodes","sim_time","created","started","relayed","aborted","dropped","removed","delivery_prob","response_prob","overhead_ratio","latency_avg","latency_med","hopcount_avg","hopcount_med","buffertime_avg","buffertime_med","rtt_avg","rtt_med"]]

for routing_dir in os.listdir(args.input):
    for bucket_dir in os.listdir(os.path.join(args.input,routing_dir)):
        if bucket_dir.endswith(".txt"):
            continue
        for MS_File in os.listdir(os.path.join(args.input,routing_dir,bucket_dir,"movement_models")):
            if(not fnmatch.fnmatch(MS_File,pattern)):
                continue
            bucket_policy=bucket_dir.split("-")[0]
            send_policy=bucket_dir.split("-")[1]
            drop_policy=bucket_dir.split("-")[2]
            movement_model = MS_File.split(".")[0]
            count_nodes = MS_File.split("_")[1]
            run_index = routing_dir.split("_")[1]
            routing_algo = routing_dir.split("_")[0]
            try:
                values = extract_values_from_file(os.path.join(os.getcwd(),args.input,routing_dir,bucket_dir,"movement_models",MS_File))
                output.append([routing_algo,run_index,movement_model,bucket_policy,send_policy,drop_policy,count_nodes,values["sim_time"],values["created"],values["started"],values["relayed"],values["aborted"],values["dropped"],values["removed"],values["delivery_prob"],values["response_prob"],values["overhead_ratio"],values["latency_avg"],values["latency_med"],values["hopcount_avg"],values["hopcount_med"],values["buffertime_avg"],values["buffertime_med"],values["rtt_avg"],values["rtt_med"]])
            except:
                print("Failed for %s" % os.path.join(os.getcwd(),args.input,routing_dir,bucket_dir,"movement_models",MS_File))

with open(os.path.join(os.getcwd(),args.output,"messageStatsReports.csv"), 'w+', newline="\n") as f:
    writer = csv.writer(f)
    for row in output:
        writer.writerow(row)
    print("Created outputfile %s" % os.path.join(os.getcwd(),args.output,"messageStatsReports.csv"))
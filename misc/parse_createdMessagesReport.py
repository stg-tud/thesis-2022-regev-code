import os
import csv
import argparse
import json

parser = argparse.ArgumentParser(description='Parse selected .txt files in a directory.')
parser.add_argument('--input', type=str, required=True, help='the path to the directory')
parser.add_argument('--output', type=str, required=True, help='the path to the directory where the result .csv is saved')
args = parser.parse_args()
if(args.output.endswith(".csv")):
    output_path = os.path.join(os.getcwd(),args.output)
else:
    output_path = os.path.join(os.getcwd(),args.output,"cp_" + os.path.basename(args.input).split(".one")[0] + ".csv")



def parse_delivery_messages(path):
    contact_counts = {}
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        next(reader)
        for row in reader:
            if row[3] <= row[4]:
                delivery = "%s<->%s" % (row[3],row[4])
            else:
                delivery = "%s<->%s" % (row[3],row[4])
            if delivery in contact_counts:
                contact_counts[delivery] += 1
            else:
                contact_counts[delivery] = 1
    return contact_counts

def write_file(res):
    tmp = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
    js = json.dumps(tmp)
    with open(output_path, "w+") as outfile:
        outfile.write("pair,contact_times")
        for key,val in tmp.items():
            outfile.write("\n%s,%s" % (key,val))
    print("Written output to: %s" % output_path)

contacts = parse_delivery_messages(args.input)
write_file(contacts)

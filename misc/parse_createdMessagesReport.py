import os
import csv
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description='Parse selected .txt files in a directory.')
parser.add_argument('--input', type=str, required=True, help='the path to the directory or file')
parser.add_argument('--output', type=str, required=True, help='the path to the directory where the result .csv is saved')
parser.add_argument('--recursive', action=argparse.BooleanOptionalAction, help='Find files recursively and process them')
args = parser.parse_args()

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

def write_file(res , output):
    tmp = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
    js = json.dumps(tmp)
    with open(output, "w+") as outfile:
        outfile.write("pair,contact_times")
        for key,val in tmp.items():
            outfile.write("\n%s,%s" % (key,val))
    print("Written output to: %s" % output)



if(args.recursive):
    if not os.path.isdir(os.path.join(os.getcwd(),args.input)) or not os.path.isdir(os.path.join(os.getcwd(),args.output)):
        raise ValueError("Provide input and output directories for recursive actions")
    if not os.path.exists(os.path.join(os.getcwd(),args.output,"output_policies")):
        os.mkdir(os.path.join(os.getcwd(),args.output,"output_policies"))
    output_path = os.path.join(os.getcwd(),args.output,"output_policies")
    for path in Path(args.input).rglob('*_CreatedMessagesReport.txt'):
        contacts = parse_delivery_messages(path)
        write_file(contacts, os.path.join(output_path,"cp_" + os.path.basename(path).split(".one")[0] + ".csv"))
else:
    if not os.path.isfile(os.path.join(os.getcwd(),args.input)):
        raise ValueError("Provide input file, not directory")
    if(args.output.endswith(".csv")):
        output_path = os.path.join(os.getcwd(),args.output)
    else:
        output_path = os.path.join(os.getcwd(),args.output,"cp_" + os.path.basename(args.input).split(".one")[0] + ".csv")
    contacts = parse_delivery_messages(args.input)
    write_file(contacts, output_path)

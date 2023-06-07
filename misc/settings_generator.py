import os
import argparse
import random

parser = argparse.ArgumentParser(description='Generates distinct setting files from big ones')
parser.add_argument('--input', type=str, help='the path to the directory containing the settings')
parser.add_argument('--output', type=str, help='path where distinct settings should be generated')
args = parser.parse_args()


def extract_values_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    values = {}
    for line in lines:
        if line.startswith("#"):
            continue
        if '=' in line:
            key, value = line.strip().split('=')
            values[key.strip()] = value.strip()

    return values

def generate_file(values, rA, bP, dP, sP, mM):
    conf = ""
    filename = "tmp-conf" + str(random.randint(1000000,999999999)) + ".txt"
    for k,i in values.items():
        if k == "Group.router":
            conf += "%s = %s\n" % (k,rA)
        elif k == "Group.BucketPolicy":
            conf += "%s = %s\n" % (k,bP)
            if bP == "staticFriendlyHostsBucketPolicy":
                conf += "%s = %s\n" % ("Group.contactPolicy","cp_" + mM.split("/")[-1].replace(".one",".csv"))
        elif k == "Group.DropPolicy":
            conf += "%s = %s\n" % (k,dP)
        elif k == "Group.SendingPolicy":
            conf += "%s = %s\n" % (k,sP)
        elif k == "ExternalMovement.file":
            conf += "%s = %s\n" % (k,mM)
        else:
            conf += "%s = %s\n" % (k,i)
    with open(os.path.join(args.output,filename), 'w+') as out:
        out.write(conf)


for settingsFile in os.listdir(args.input):
    values = extract_values_from_file(os.path.join(args.input,settingsFile))
    routingAlgorithms = values["Group.router"].replace("[","").replace("]","").split(";")
    bucketPolicies = values["Group.BucketPolicy"].replace("[","").replace("]","").split(";")
    dropPolicies = values["Group.DropPolicy"].replace("[","").replace("]","").split(";")
    sendingPolicies =  values["Group.SendingPolicy"].replace("[","").replace("]","").split(";")
    movementModels = values["ExternalMovement.file"].replace("[","").replace("]","").split(";")
    
    for routingAlgo in routingAlgorithms:
        for bucketPolicy in bucketPolicies:
            for dropPolicy in dropPolicies:
                for sendingPolicy in sendingPolicies:
                    for movementModel in movementModels:
                        generate_file(values,routingAlgo,bucketPolicy,dropPolicy,sendingPolicy,movementModel)
print("Sucessfully generated setting files!")




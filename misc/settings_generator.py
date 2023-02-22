import os
import pathlib


abspath = pathlib.Path(__file__).parent.resolve()
bp = os.path.join(abspath,"generated_configs")

list_routing_algorithms = ["EpidemicRouter","SprayAndWaitRouter"]
list_bufferpolicies= ["destinationBasedBucketPolicy", "forwardCountBucketPolicy","friendlyHostsBucketPolicy",
"prioritizeLowTTLBucketPolicy", "randomBucketPolicy", "roundRobinBucketPolicy", "senderBasedBucketAssignmentPolicy",
"sizeBasedBucketsPolicy","sourceSegregationBucketPolicy"]
list_sendingpolicies = ["FIFOsendPolicy"]
list_droppolicies = ["default"]

for routing_algorithm in list_routing_algorithms:
    for bufferpolicy in list_bufferpolicies:
        for sendingpolicy in list_sendingpolicies:
            for droppolicy in list_droppolicies:
                if os.path.exists(os.path.join(bp,routing_algorithm)) == False:
                    os.mkdir(os.path.join(bp,routing_algorithm))
                filename="%s_%s_%s_%s.txt" % (routing_algorithm,bufferpolicy,sendingpolicy,droppolicy)
                with open(os.path.join(bp,routing_algorithm,filename), "w+") as file:
                    file.write("Scenario.name = Routing %s Buffer %s Sending %s Drop %s\n" % (routing_algorithm,bufferpolicy,sendingpolicy,droppolicy))
                    file.write("Group.router = %s\n" % (routing_algorithm))
                    if bufferpolicy != "default":
                        file.write("Group.BucketPolicy = %s\n" % (bufferpolicy))
                    if sendingpolicy != "default":
                        file.write("Group.SendingPolicy = %s\n" % (sendingpolicy))
                    if droppolicy != "default":
                        file.write("Group.DropPolicy = %s\n" % (sendingpolicy))
                        


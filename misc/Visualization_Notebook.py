#!/usr/bin/env python
# coding: utf-8

# In[1]:


for var in list(globals()):
    if var.startswith('scenario'):
        del globals()[var]

    
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import seaborn as sns
import numpy as np
import warnings

csv_path=os.path.join(os.getcwd(),"eval_1408.csv")
df = pd.read_csv(csv_path, skiprows=[0])
scenario_names = []
df_runs = []
for scenario in df["SimulationID"].unique():
    scenario_names.append(scenario)
    globals()[scenario] = df.loc[df['SimulationID'] == scenario]
    
for var_name in list(globals()):
    if isinstance(globals()[var_name], pd.DataFrame) and var_name.startswith("scenario"):
        df_runs.append((var_name, globals()[var_name]))


# In[2]:


OUTPUT_BP = os.path.join(os.getcwd(),"output")
if not os.path.exists(OUTPUT_BP):
    os.makedirs(OUTPUT_BP)


# In[3]:


# Suppress all warnings
warnings.filterwarnings("ignore")


# In[4]:


print(df["BufferSize"].unique())
print(scenario_names)


# In[5]:


#SYNTAX df.loc[ (expr1) & (expr2) | ...]  => Klammern nicht vergessen
# expr: df["FIELD"] == "VALUE"

#Alternativ:
# df.loc[df["FIELD"].isin(["VALUE1",...,"VALUEN"])]   

# Kombinationen von mehreren Feldern
# Beispiel: hue=df_runs[i][["BucketPolicy","MovementModel"]].apply(tuple, axis=1)
"""
BUCKET FILTER
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]

Routing FILTER
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 

Movement Model FILTER
current_df = current_df.loc[current_df["MovementModel"].isin(['MG1_100_24h', 'MG2_100_24h', 'MG3_100_24h', 'MG4_100_24h', 'MG5_100_24h',
 'RW1_100_24h', 'RW2_100_24h', 'RW3_100_24h', 'RW4_100_24h', 'RW5_100_24h'])]
"""
("")


# In[6]:


#sns.set_theme(style="ticks" , palette=sns.color_palette("pastel", 4))
#sns.set_theme(style="ticks" , palette=sns.color_palette("tab10"))
sns.set_theme(style="ticks" , palette=sns.color_palette("bright"))


# # 
# <font size="15">Delivery Probability</font>

# <font size="5">Delivery Probability All</font>
# 

# In[7]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            try:
                plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0] ,nodecount, buffersize),
                              fontsize=24, fontdict={"weight": "bold"})
                plt.figure(plt_id)
                plt_id += 1
                current_df = df_runs[i][1]
                current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
                current_df = current_df.loc[current_df["Nodes"].isin([nodecount])]

                boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                            hue="BucketPolicy",
                            data= current_df)
                boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
                sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))


            except:
                pass


# <font size="5">Delivery Probability by Drop Policy</font>

# In[8]:


plot_path = os.path.join(OUTPUT_BP,"dp_drop")
if not os.path.exists(plot_path):
    os.makedirs(plot_path)
plt_id = 0
savefig = True

for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            try:           
                plt.figure(plt_id)
                if not savefig:
                    plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                              fontsize=24, fontdict={"weight": "bold"})
                plt_id += 1
                current_df = df_runs[i][1]
                current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
                current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 


                stripplot = sns.stripplot(x="RoutingAlgorithm", y="delivery_prob",
                            hue="DropPolicy",
                            data=current_df,
                            dodge=True
                            )

                sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
                if savefig:
                    #plt.legend('',frameon=False)
                    plt.ylim(0, 1)
                    plt.ylabel("Delivery Probability")
                    plt.xlabel("Drop Policy")
                    plt.xticks(rotation=45)
                    plt.savefig(os.path.join(plot_path,"%s_%dnodes_%sbuf.svg" % (df_runs[i][0], nodecount, buffersize)), bbox_inches='tight' ,format='svg')

            except:
                pass


# <font size="5">Delivery Probability for distinct Bucket Policy</font>

# In[9]:


plt_id = 0
OUTPUT_BP = os.path.join(os.getcwd(),"output")
if not os.path.exists(OUTPUT_BP):
    os.makedirs(OUTPUT_BP)
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]


            #['dropFrontPolicy' 'dropLargestPolicy' 'dropLastPolicy' 'dropOldestPolicy','dropYoungestPolicy']
            current_df = current_df.loc[(current_df["DropPolicy"]).isin(["dropLargestPolicy"])]



            boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                        hue="BucketPolicy",
                        data=current_df )

            boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
            sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Delivery Probability for distinct Sending Policy</font>

# In[10]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]


            #['dropFrontPolicy' 'dropLargestPolicy' 'dropLastPolicy' 'dropOldestPolicy','dropYoungestPolicy']
            current_df = current_df.loc[(current_df["DropPolicy"]).isin(["dropLargestPolicy"])]



            boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                        hue="SendPolicy",
                        data=current_df )

            boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
            sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Delivery Probability by Drop + Bucket Combination</font>

# In[11]:


enable = False
if enable:
    plt_id = 0
    for i in range(len(df_runs)):
        for buffersize in sorted(df["BufferSize"].unique()):
            for nodecount in sorted(df["Nodes"].unique()):
                plt.figure(plt_id)
                plt_id += 1
                current_df = df_runs[i][1]
                current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
                current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

                #Filter for Routing Algorithm
                current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
                #Filter for Bucket Policy
                current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
                 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
                 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
                 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
                 'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]

                current_df = current_df.sort_values(by='DropPolicy')



                stripplot = sns.stripplot(x="RoutingAlgorithm", y="delivery_prob",
                            hue=current_df[["DropPolicy","BucketPolicy"]].apply(tuple, axis=1),
                            data=current_df, dodge=True, linewidth=0.5)

                sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
                plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                              fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Delivery Probability for distinct Router AND Drop + Bucket Combination</font>

# In[12]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]

            stripplot = sns.stripplot(x="DropPolicy", y="delivery_prob",
                        hue="BucketPolicy",
                        data=current_df, dodge=True, linewidth=0.5)
            try:
                stripplot.set_xticklabels(stripplot.get_xticklabels(),rotation=30)
                sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
                plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})
            except:
                pass


# <font size="5">Delivery Probability for distinct Router AND Drop + Send Combination</font>

# In[13]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]

            stripplot = sns.stripplot(x="DropPolicy", y="delivery_prob",
                        hue="SendPolicy",
                        data=current_df, dodge=True, linewidth=0.5)
            try:
                stripplot.set_xticklabels(stripplot.get_xticklabels(),rotation=30)
                sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
                plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})
            except:
                pass


# <font size="5">Latency Median</font>

# In[14]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 
            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                             'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]


            boxplot = sns.boxplot(x="RoutingAlgorithm", y="latency_avg",
                        hue="BucketPolicy",
                        data=current_df )

            boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
            sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Latency AVG by Drop Policy</font>

# In[15]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                             'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]

            """
            sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                        hue="DropPolicy",
                        data=current_df,                   
                       )
            """

            stripplot = sns.stripplot(x="RoutingAlgorithm", y="latency_avg",
                        hue="DropPolicy",
                        data=current_df,
                        dodge=True            
                        )


            sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Latency AVG by Sending Policy</font>

# In[16]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                             'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
            #Filter for Bucket Policy
            """
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]
             """
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy']))]

            """
            sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                        hue="DropPolicy",
                        data=current_df,                   
                       )
            """

            stripplot = sns.stripplot(x="RoutingAlgorithm", y="latency_avg",
                        hue="SendPolicy",
                        data=current_df,
                        dodge=True            
                        )


            sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Overhead Ratio</font>

# In[17]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 
            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                             'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]


            boxplot = sns.boxplot(x="RoutingAlgorithm", y="overhead_ratio",
                        hue="BucketPolicy",
                        data=current_df )

            boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
            sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Overhead Ratio by Drop Policy</font>

# In[18]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                             'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]

            """
            sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                        hue="DropPolicy",
                        data=current_df,                   
                       )
            """

            stripplot = sns.stripplot(x="RoutingAlgorithm", y="overhead_ratio",
                        hue="DropPolicy",
                        data=current_df,
                        dodge=True            
                        )


            sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Overhead Ratio by Sending Policy</font>

# In[19]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                             'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])]
            current_df = current_df.loc[current_df["DropPolicy"].isin(['dropHeadPolicy'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy']))]

            """
            sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                        hue="DropPolicy",
                        data=current_df,                   
                       )
            """

            stripplot = sns.stripplot(x="RoutingAlgorithm", y="overhead_ratio",
                        hue="SendPolicy",
                        data=current_df,
                        dodge=True            
                        )


            sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# In[ ]:





# In[26]:


plt_id = 0
for i in range(len(df_runs)):
    for buffersize in sorted(df["BufferSize"].unique()):
        for nodecount in sorted(df["Nodes"].unique()):
            plt.figure(plt_id)
            plt_id += 1
            current_df = df_runs[i][1]
            current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
            current_df = current_df.loc[current_df["Nodes"].isin([nodecount])] 

            #Filter for Routing Algorithm
            current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                             'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
            #Filter for Bucket Policy
            current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
             'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
             'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
             'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
             'sourceSegregationBucketPolicy','staticFriendlyHostsBucketPolicy']))]

            """
            sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                        hue="DropPolicy",
                        data=current_df,                   
                       )
            """

            stripplot = sns.stripplot(x="RoutingAlgorithm", y="hopcount_avg",
                        hue="DropPolicy",
                        data=current_df,
                        dodge=True            
                        )


            sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
            plt.suptitle("Scenario: %s Nodes: %d Buffer: %s" % (df_runs[i][0], nodecount, buffersize),
                          fontsize=24, fontdict={"weight": "bold"})


# # 
# <font size="15">Backup</font>

# In[20]:


stopper


# In[ ]:


"""
for i in range(len(df_runs)):
    plt.figure(i)
    
    boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                hue="BucketPolicy",
                data=df_runs[i][1] )
    boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
    sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))
    plt.suptitle(df_runs[i][0],
                  fontsize=24, fontdict={"weight": "bold"})
"""
("")


# Nodes + Drop

# In[14]:


active = True
savefig = True

palette = {
    "L": 'tab:red',
    "M": 'tab:orange',
    "S": 'tab:green',
}

if active:
    plot_path = os.path.join(OUTPUT_BP,"dp_drop")
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    plt_id = 0
    df['DropPolicy'] = df['DropPolicy'].str.replace("dropFrontPolicy","Drop Front").replace("dropHeadPolicy","Drop Head").replace("dropLargestPolicy","Drop Largest").replace("dropLastPolicy","Drop Last").replace("dropRandomPolicy","Drop Random").replace("dropYoungestPolicy","Drop Youngest").replace("mofoPolicy","MOFO").replace("shliPolicy","SHLI")
    #for i in df["Scenario"].unique():
    for i in ["scenario3"]:
        for buffersize in sorted(df["BufferSize"].unique()):
                    plt.figure(plt_id)
                    if not savefig:
                        plt.suptitle("Scenario: %s  Buffer: %s" % (df_runs[i][0], buffersize),
                                  fontsize=24, fontdict={"weight": "bold"})
                    plt_id += 1
                    current_df = df.loc[df["Scenario"].isin([i])] 
                    current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])]
                    
                    stripplot = sns.swarmplot(x="DropPolicy", y="delivery_prob",hue="WorldSize",
                                data=current_df,palette=palette)
                    
                    stripplot.set_xticklabels(stripplot.get_xticklabels(),rotation=45)

                    sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
                    if savefig:
                        """
                        plt.legend('',frameon=False)
                        
                        """
                        plt.ylim(0, 1)
                        plt.ylabel("Delivery Probability")
                        #plt.xlabel("Drop Policy")
                        #plt.xticks(rotation=45)
                        
                        plt.savefig(os.path.join(plot_path,"%s_%s_swarm-buf-worldsizes.svg" % (i, buffersize)), bbox_inches='tight' ,format='svg')


# In[15]:


active = True
savefig = True

palette = {
    100: 'tab:red',
    50: 'tab:orange',
    25: 'tab:green',
}

if active:
    plot_path = os.path.join(OUTPUT_BP,"dp_drop")
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    plt_id = 0
    for i in range(len(df_runs)):
        df_runs[i][1]['DropPolicy'] = df_runs[i][1]['DropPolicy'].str.replace("dropFrontPolicy","Drop Front").replace("dropHeadPolicy","Drop Head").replace("dropLargestPolicy","Drop Largest").replace("dropLastPolicy","Drop Last").replace("dropRandomPolicy","Drop Random").replace("dropYoungestPolicy","Drop Youngest").replace("mofoPolicy","MOFO").replace("shliPolicy","SHLI")
        for buffersize in sorted(df["BufferSize"].unique()):
                    plt.figure(plt_id)
                    if not savefig:
                        plt.suptitle("Scenario: %s  Buffer: %s" % (df_runs[i][0], buffersize),
                                  fontsize=24, fontdict={"weight": "bold"})
                    plt_id += 1
                    current_df = df_runs[i][1]
                    current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
                    current_df = current_df.loc[current_df["Nodes"].isin([100])] 
                    
                    stripplot = sns.swarmplot(x="DropPolicy", y="delivery_prob",
                                data=current_df)
                    
                    stripplot.set_xticklabels(stripplot.get_xticklabels(),rotation=45)

                    #sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
                    if savefig:
                        """
                        plt.legend('',frameon=False)
                        
                        """
                        plt.ylim(0, 1)
                        plt.ylabel("Delivery Probability")
                        #plt.xlabel("Drop Policy")
                        #plt.xticks(rotation=45)
                        
                        plt.savefig(os.path.join(plot_path,"%s_%s_100n-swarm-buf.svg" % (df_runs[i][0], buffersize)), bbox_inches='tight' ,format='svg')


# In[18]:


active = True
savefig = True

palette = {
    100: 'tab:red',
    50: 'tab:orange',
    25: 'tab:green',
}

if active:
    plot_path = os.path.join(OUTPUT_BP,"dp_drop")
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    plt_id = 0
    for i in range(len(df_runs)):
        df_runs[i][1]['DropPolicy'] = df_runs[i][1]['DropPolicy'].str.replace("dropFrontPolicy","Drop Front").replace("dropHeadPolicy","Drop Head").replace("dropLargestPolicy","Drop Largest").replace("dropLastPolicy","Drop Last").replace("dropRandomPolicy","Drop Random").replace("dropYoungestPolicy","Drop Youngest").replace("mofoPolicy","MOFO").replace("shliPolicy","SHLI")
        for buffersize in sorted(df["BufferSize"].unique()):
                    plt.figure(plt_id)
                    if not savefig:
                        plt.suptitle("Scenario: %s  Buffer: %s" % (df_runs[i][0], buffersize),
                                  fontsize=24, fontdict={"weight": "bold"})
                    plt_id += 1
                    current_df = df_runs[i][1]
                    current_df = current_df.loc[current_df["BufferSize"].isin([buffersize])] 
                    
                    stripplot = sns.swarmplot(x="DropPolicy", y="delivery_prob",hue="Nodes",
                                data=current_df,palette=palette)
                    
                    stripplot.set_xticklabels(stripplot.get_xticklabels(),rotation=45)

                    sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
                    if savefig:
                        """
                        plt.legend('',frameon=False)
                        
                        """
                        plt.ylim(0, 1)
                        plt.ylabel("Delivery Probability")
                        #plt.xlabel("Drop Policy")
                        #plt.xticks(rotation=45)
                        
                        plt.savefig(os.path.join(plot_path,"%s_%s-swarm-buf.svg" % (df_runs[i][0], buffersize)), bbox_inches='tight' ,format='svg')


# 

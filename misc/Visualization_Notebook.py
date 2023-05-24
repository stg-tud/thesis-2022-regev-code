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

csv_path=os.path.join(os.getcwd(),"messageStatsReports_relevant.csv")
df = pd.read_csv(csv_path, skiprows=[0])
scenario_names = []
df_runs = []
for scenario in df["Scenario"].unique():
    scenario_names.append(scenario)
    globals()[scenario] = df.loc[df['Scenario'] == scenario]
    
for var_name in list(globals()):
    if isinstance(globals()[var_name], pd.DataFrame) and var_name.startswith("scenario"):
        df_runs.append((var_name, globals()[var_name]))


# In[2]:


print(df["Scenario"].unique())


# In[3]:


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
 'sourceSegregationBucketPolicy']))]

Routing FILTER
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 

Movement Model FILTER
current_df = current_df.loc[current_df["MovementModel"].isin(['MG1_100_24h', 'MG2_100_24h', 'MG3_100_24h', 'MG4_100_24h', 'MG5_100_24h',
 'RW1_100_24h', 'RW2_100_24h', 'RW3_100_24h', 'RW4_100_24h', 'RW5_100_24h'])]
"""
("")


# In[4]:


print(df_runs)


# In[5]:


#sns.set_theme(style="ticks" , palette=sns.color_palette("pastel", 4))
#sns.set_theme(style="ticks" , palette=sns.color_palette("tab10"))
sns.set_theme(style="ticks" , palette=sns.color_palette("bright"))


# # 
# <font size="15">Delivery Probability</font>

# <font size="5">Delivery Probability All</font>
# 

# In[6]:


for i in range(len(df_runs)):
    plt.figure(i)
    
    boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                hue="BucketPolicy",
                data=df_runs[i][1] )
    boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
    sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))
    plt.suptitle("Run" + df_runs[i][0],
                  fontsize=24, fontdict={"weight": "bold"})


# <font size="5">Delivery Probability by Drop Policy</font>

# In[7]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

"""
sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
            hue="DropPolicy",
            data=current_df,                   
           )
"""

stripplot = sns.stripplot(x="RoutingAlgorithm", y="delivery_prob",
            hue="DropPolicy",
            data=current_df,
            dodge=True            
            )


sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))


# <font size="5">Delivery Probability for distinct Drop Policy</font>

# In[8]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

#['dropFrontPolicy' 'dropLargestPolicy' 'dropLastPolicy' 'dropOldestPolicy','dropYoungestPolicy']
current_df = current_df.loc[(current_df["DropPolicy"]).isin(["dropLargestPolicy"])]



boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
            hue="BucketPolicy",
            data=current_df )

boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))


# <font size="5">Delivery Probability by Drop + Bucket Combination</font>

# In[9]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

current_df = current_df.sort_values(by='DropPolicy')



stripplot = sns.stripplot(x="RoutingAlgorithm", y="delivery_prob",
            hue=current_df[["DropPolicy","BucketPolicy"]].apply(tuple, axis=1),
            data=current_df, dodge=True, linewidth=0.5)

sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))


# <font size="5">Delivery Probability for distinct Router AND Drop + Bucket Combination</font>

# In[10]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]



stripplot = sns.stripplot(x="DropPolicy", y="delivery_prob",
            hue="BucketPolicy",
            data=current_df, dodge=True, linewidth=0.5)
try:
    stripplot.set_xticklabels(stripplot.get_xticklabels(),rotation=30)
    sns.move_legend(stripplot , "upper left", bbox_to_anchor=(1, 1))
except:
    pass


# <font size="5">Latency Median</font>

# In[11]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]


boxplot = sns.boxplot(x="RoutingAlgorithm", y="latency_avg",
            hue="BucketPolicy",
            data=current_df )

boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))


# <font size="5">Latency AVG by Drop Policy</font>

# In[12]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

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


# <font size="5">Overhead Ratio</font>

# In[13]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]


boxplot = sns.boxplot(x="RoutingAlgorithm", y="overhead_ratio",
            hue="BucketPolicy",
            data=current_df )

boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))


# <font size="5">Overhead Ratio by Drop Policy</font>

# In[14]:


# Filter for RUN ID
current_df = scenarioEPIDEMIC_D

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

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


# In[ ]:




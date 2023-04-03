#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import seaborn as sns


# In[2]:


csv_path=os.path.join(os.getcwd(),"messageStatsReports.csv")
#csv_path=os.path.join(os.getcwd(),"messageStatsReports_smallBuffer.csv")


# In[3]:


#read csv
df = pd.read_csv(csv_path, skiprows=[0])
df_runa = df.loc[df['RunID'] == "runa"]
df_runb = df.loc[df['RunID'] == "runb"]
df_runc = df.loc[df['RunID'] == "runc"]
df_runs = [df_runa,df_runb,df_runc]

epidemicVSsnw = ['EpidemicRouter', 'SprayAndWaitRouter-7f', 'SprayAndWaitRouter-7t']
epidemicVSprophet = ['EpidemicRouter', 'ProphetRouter', 'ProphetV2Router']


#SYNTAX df.loc[ (expr1) & (expr2) | ...]  => Klammern nicht vergessen
# expr: df["FIELD"] == "VALUE"

#Alternativ:
# df.loc[df["FIELD"].isin(["VALUE1",...,"VALUEN"])]   

# Kombinationen von mehreren Feldern
# Beispiel: hue=df_runs[i][["BucketPolicy","MovementModel"]].apply(tuple, axis=1)


# In[4]:


"""
BUCKET FILTER
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]
"""

"""
Routing FILTER
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
"""
"""
Movement Model FILTER
current_df = current_df.loc[current_df["MovementModel"].isin(['MG1_100_24h', 'MG2_100_24h', 'MG3_100_24h', 'MG4_100_24h', 'MG5_100_24h',
 'RW1_100_24h', 'RW2_100_24h', 'RW3_100_24h', 'RW4_100_24h', 'RW5_100_24h'])]
"""
("")


# In[5]:


#print(df.head(0))
print(df["MovementModel"].unique())


# In[6]:


sns.set_theme(style="ticks" , palette=sns.color_palette("pastel", 4))


# # 
# <font size="15">Boxplots</font>

# <font size="5">Delivery Probability</font>
# 

# In[7]:


for i in range(len(df_runs)):
    plt.figure(i)
    
    boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                hue="BucketPolicy",
                data=df_runs[i] )
    boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
    sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))


# In[8]:


# Filter for RUN ID
current_df = df_runa

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]


boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
            hue="BucketPolicy",
            data=current_df )

boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))


# <font size="5">Latency Median</font>

# In[9]:


# Filter for RUN ID
current_df = df_runa

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]


boxplot = sns.boxplot(x="RoutingAlgorithm", y="latency_med",
            hue="BucketPolicy",
            data=current_df )

boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))


# <font size="5">Overhead Ratio</font>

# In[10]:


# Filter for RUN ID
current_df = df_runa

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


# # 
# <font size="15">Scatterplot</font>

# <font size="5">Delivery Probability</font>

# In[11]:


for i in range(len(df_runs)):
    plt.figure(i)
    scatterplot = sns.scatterplot(y="RoutingAlgorithm", x="delivery_prob",
                hue="BucketPolicy",
                data=df_runs[i])
    try:
        sns.move_legend(scatterplot , "upper left", bbox_to_anchor=(1, 1))
    except:
        continue
    


# In[12]:


# Filter for RUN ID
current_df = df_runa

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

#Filter for Movement Model
current_df = current_df.loc[current_df["MovementModel"].isin(['MG1_100_24h', 'MG2_100_24h', 'MG3_100_24h', 'MG4_100_24h', 'MG5_100_24h',
 'RW1_100_24h', 'RW2_100_24h', 'RW3_100_24h', 'RW4_100_24h', 'RW5_100_24h'])]

scatterplot = sns.scatterplot(y="RoutingAlgorithm", x="delivery_prob",
                hue="BucketPolicy",
                data=current_df)

sns.move_legend(scatterplot , "upper left", bbox_to_anchor=(1, 1))


    


# <font size="5">Latency Med</font>

# In[13]:


# Filter for RUN ID
current_df = df_runa

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

#Filter for Movement Model
current_df = current_df.loc[current_df["MovementModel"].isin(['MG1_100_24h', 'MG2_100_24h', 'MG3_100_24h', 'MG4_100_24h', 'MG5_100_24h',
 'RW1_100_24h', 'RW2_100_24h', 'RW3_100_24h', 'RW4_100_24h', 'RW5_100_24h'])]

scatterplot = sns.scatterplot(y="RoutingAlgorithm", x="latency_med",
                hue="BucketPolicy",
                data=current_df)

sns.move_legend(scatterplot , "upper left", bbox_to_anchor=(1, 1))


    


# <font size="5">Buffertime Med</font>

# In[14]:


# Filter for RUN ID
current_df = df_runa

#Filter for Routing Algorithm
current_df = current_df.loc[current_df["RoutingAlgorithm"].isin(['EpidemicRouter', 'SprayAndWaitRouter-7f',
                                                                 'SprayAndWaitRouter-7t','ProphetRouter', 'ProphetV2Router'])] 
#Filter for Bucket Policy
current_df = current_df.loc[(current_df["BucketPolicy"].isin(['DefaultBucketAssignmentPolicy','destinationBasedBucketPolicy',
 'forwardCountBucketPolicy','friendlyHostsBucketPolicy',
 'prioritizeLowTTLBucketPolicy','randomBucketPolicy',
 'roundRobinBucketPolicy','senderBasedBucketAssignmentPolicy',
 'sourceSegregationBucketPolicy']))]

#Filter for Movement Model
current_df = current_df.loc[current_df["MovementModel"].isin(['MG1_100_24h', 'MG2_100_24h', 'MG3_100_24h', 'MG4_100_24h', 'MG5_100_24h',
 'RW1_100_24h', 'RW2_100_24h', 'RW3_100_24h', 'RW4_100_24h', 'RW5_100_24h'])]

scatterplot = sns.scatterplot(y="RoutingAlgorithm", x="overhead_ratio",
                hue="BucketPolicy",
                data=current_df)

sns.move_legend(scatterplot , "upper left", bbox_to_anchor=(1, 1))


    


#!/usr/bin/env python
# coding: utf-8

# In[66]:


for var in list(globals()):
    del globals()[var]
    
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import seaborn as sns


# In[67]:


csv_path=os.path.join(os.getcwd(),"messageStatsReports_Epidemic.csv")
df = pd.read_csv(csv_path, skiprows=[0])


# In[68]:


print(df["Scenario"].unique())


# In[70]:


scenario_names = []
df_runs = []
for scenario in df["Scenario"].unique():
    scenario_names.append(scenario)
    globals()[scenario] = df.loc[df['Scenario'] == scenario]
    
for var_name in globals():
    if isinstance(globals()[var_name], pd.DataFrame) and var_name.startswith("scenario"):
        df_runs.append((var_name, globals()[var_name]))


#SYNTAX df.loc[ (expr1) & (expr2) | ...]  => Klammern nicht vergessen
# expr: df["FIELD"] == "VALUE"

#Alternativ:
# df.loc[df["FIELD"].isin(["VALUE1",...,"VALUEN"])]   

# Kombinationen von mehreren Feldern
# Beispiel: hue=df_runs[i][["BucketPolicy","MovementModel"]].apply(tuple, axis=1)


# In[59]:


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


# In[74]:


sns.set_theme(style="ticks" , palette=sns.color_palette("pastel", 4))


# # 
# <font size="15">Boxplots</font>

# <font size="5">Delivery Probability</font>
# 

# In[75]:


for i in range(len(df_runs)):
    plt.figure(i)
    
    boxplot = sns.boxplot(x="RoutingAlgorithm", y="delivery_prob",
                hue="BucketPolicy",
                data=df_runs[i][1] )
    boxplot.set_xticklabels(boxplot.get_xticklabels(),rotation=30)
    sns.move_legend(boxplot , "upper left", bbox_to_anchor=(1, 1))
    plt.suptitle("Run" + df_runs[i][0],
                  fontsize=24, fontdict={"weight": "bold"})


# In[76]:


# Filter for RUN ID
current_df = scenarioL

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

# In[77]:


# Filter for RUN ID
current_df = scenarioL

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


# <font size="5">Overhead Ratio</font>

# In[78]:


# Filter for RUN ID
current_df = scenarioL

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

# In[80]:


for i in range(len(df_runs)):
    # Filter for direct comparison

    plt.figure(i)
    scatterplot = sns.scatterplot(y="RoutingAlgorithm", x="delivery_prob",
                hue="BucketPolicy",
                data=df_runs[i][1])
    plt.suptitle("Run" + df_runs[i][0],
                  fontsize=24, fontdict={"weight": "bold"})
    try:
        sns.move_legend(scatterplot , "upper left", bbox_to_anchor=(1, 1))
        
    except:
        continue
    


# In[81]:


# Filter for RUN ID
current_df = scenarioL

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

# In[82]:


# Filter for RUN ID
current_df = scenarioL

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

# In[83]:


# Filter for RUN ID
current_df = scenarioL

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


    


# # 
# <font size="15">Relplot</font>

# In[84]:


# Filter for RUN ID
current_df = scenarioL

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

for i,routingAlgo in enumerate(current_df["RoutingAlgorithm"].unique()):
    plt.figure(i)
    ax = sns.relplot(
        data=current_df, x="MovementModel", y="delivery_prob",
        hue="BucketPolicy", kind="line",
    )
    ax.fig.suptitle(routingAlgo,
                  fontsize=24, fontdict={"weight": "bold"})
    ax.tick_params(axis='x', rotation=90)


# In[ ]:





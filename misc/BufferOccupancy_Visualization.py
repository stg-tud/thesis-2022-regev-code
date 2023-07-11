#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from pathlib import Path


# In[2]:


addresses = pd.DataFrame(columns=['path','scenario','mm','size','rw','nodes','duration','bucketPolicy','sendingPolicy','dropPolicy','bufferSize'])
for path in Path(os.path.join(os.getcwd(),"..","eval_020723")).rglob('*_BufferOccupancyReport.txt'):
    mm = str(path).split(".one")[0].split("\\")[-1]
    size,rw, nodes,duration = mm.split("_")
    scenario = str(path).split("scenario")[-1][0]
    bucket,sending,drop,buffer = str(path).split("\\")[-3].split("-")[:4]
    addresses.loc[len(addresses)]={'path':path,'scenario':scenario,'mm':mm,'size':size,'rw':rw,'nodes':nodes,'duration':duration,'bucketPolicy':bucket,'sendingPolicy':sending,'dropPolicy':drop,'bufferSize':buffer}


# In[11]:


def read_buffer_report(bufferReport):
    df = pd.read_csv(bufferReport, header=None, sep='\s', engine='python')
    return df


# In[19]:


current_df = addresses.loc[addresses["bufferSize"].isin(["256k"])]
current_df = current_df.loc[addresses["size"].isin(["S"])]
current_df = current_df.loc[addresses["nodes"].isin(["50"])]
current_df = current_df.loc[addresses["rw"].isin(["RW1"])]
current_df = current_df.loc[addresses["dropPolicy"].isin(["dropYoungestPolicy"])]
#current_df = current_df.loc[addresses["bucketPolicy"].isin(["DefaultBucketAssignmentPolicy"])]
current_df = current_df.loc[addresses["scenario"].isin(["3"])]



for _, address in current_df.iterrows():
    name = "%s_%s_%s_%s_%s" % (address["scenario"],mm,address["dropPolicy"],address["bucketPolicy"],address["sendingPolicy"])
    df = read_buffer_report(address["path"])
    lineplot = sns.lineplot(x=0, y=1, data=df, label=name)

plt.ylim(0, 100)
lineplot.set(ylabel="Buffer Occupancy in %", xlabel="Time in sec", title="Buffer Occupancy by Scenario")
sns.move_legend(lineplot , "upper left", bbox_to_anchor=(1, 1))


# In[ ]:





# In[ ]:





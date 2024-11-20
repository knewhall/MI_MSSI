import numpy as np
import pandas as pd 


# ---- compute increments ------
#non overlapping intervals, takes in two dimensional path as dataframe, 
#starts increments from top of time serires 
def difference_indep2(dataset, interval):
    
    diff = list()
    data = np.asarray(pd.concat([dataset['X'],dataset['Y']],axis=1))
   
    if (len(dataset) % interval) == 0:
        X=1
    else:
        X=0
    k=0    

    idx_top = int(len(dataset))-1
    idx_bottom = 0

    for i in range( int(len(dataset)/interval)-X,0,-1):
        value = data[idx_top-(i-1)*(interval),:] - data[idx_top-i*(interval),:]
        diff.append(value)
        
    return (diff)



# ----- compute MSD -------
def msd_indep2(dataset):
    #msd = np.zeros(int(len(dataset)/2))
    msd = np.zeros(int(len(dataset)-1))

    #for i in range(1,int(len(dataset)/2)):
    for i in range(1,int(len(dataset)-1)):

        sq_inc = np.square(difference_indep2(dataset,interval=i)).sum(axis=1)
        final = sq_inc.mean()
        msd[i] = final

    return(msd)
import numpy as np
import pandas as pd 

#%run ../SWIMMERS/Model/Combined-fxns-single-2D.ipynb


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


# ----- compute VCF -------
def VCF3(dataset):
    VCF_values = []  #need at least 3 points to find 2 vectors and angle between

    for i in range(1,int(len(dataset)/2)): #or divided by 3 and plus 1
        interval = i

        diff = difference_indep2(dataset,interval=interval)

        cosines= [] 
        
        for j in range(1,int(len(diff))): 

            cosines.append(np.dot(diff[j],diff[j-1])/(np.linalg.norm(diff[j])*np.linalg.norm(diff[j-1])))

        cosines=np.asarray(cosines)
        final = cosines.mean()

        VCF_values.append(final)

    VCF_values=np.asarray(VCF_values)
    
    return(VCF_values)
import pandas as pd
import numpy as np

def sample_data_timelag2(data, N, T, seed = None): # sampling of timelagged data by timestamp (not index) 
    
    #--- exit function if dataframe is empty---
    if(len(data) ==0):
        return(0)
    
    
    #--- restrict data before taking first sample (end edge case)---
    end_time = data['t'].iloc[-2] # need second to last element so while loop doesn't try to check an out of bounds condition
    data_trim = data[data['t'] <= end_time - T]
    
    # if(seed == 'off'):
    #     seed = None
    # else:
    #     seed = int(seed)
        
    #--- sample trimmed data---
    # new way, sampling with replacement if SS exceeds population size
    if(N>len(data_trim)):
        #print('sampled with replacement, population:' + str(len(data_trim)) +'<  N:' + str(N))
        replacement = True
    else:
        replacement = False
        
    # old way, has replace = False in all cases   
    sample = data_trim.sample(n = N, replace = replacement, random_state = seed)
    
    #--- store timelagged data, first as array---
    timelagged_sample = np.zeros(np.shape(sample))
    
    #--- sort sample---
    sample_sorted = sample.sort_values('t')
    sorted_indices = np.array(sample_sorted.index)
    start_times = np.array(sample_sorted['t'])

    k = 0
    for i in sorted_indices: # go through each point in original sample

        start = start_times[k] # pick time of sample point 

        target = start + T # identify end time of interval

        next_one = start # iterate over subsequent items after start time


        count = 0 # counter for while loop

        while(( next_one <= target )): # step through subsequent times until target time is reached 
            next_one = data.iloc[i + count]['t']

            count = count + 1
      
        new_data = data.iloc[i + count - 2] # pick out the timelagged data
        timelagged_sample[k,:] =  new_data # store in matrix
        
        k = k + 1

    # rewrite timelagged data as dataframe
    timelagged_sample = pd.DataFrame(data=timelagged_sample, columns=sample.columns)#, index=sample.index)
    
    # report sample after reindexing
    sample_sorted = sample_sorted.reset_index(drop=True)
    
    return(sample_sorted, timelagged_sample)
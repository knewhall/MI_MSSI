import math
import numpy as np
from multiprocessing import Pool
import pandas as pd 

from MI_Functions_Copy import compute_MI_scalar2, angle_distance, compute_MI_scalar_angles, compute_MI_scalar_mixed
from Sampling_Timelag_Copy import sample_data_timelag2
from scipy.optimize import curve_fit

# ----------COMPUTE TIMELAGGED MUTUAL INFO/ MUTUAL SELF INFORMATION-----------

straight_data_all = pd.read_csv('straight_data_ABP_V6_a.csv', index_col = 0)

MSSI_MI_all = []

#for p in range(0, 1): # for each path

def compute_MI_of_MSSI(p):
    N = 500
    T = np.logspace(-1.5,1,15)
    reps = 10 #10

    MI_data = np.zeros((reps, len(T)))
    input_data = pd.DataFrame({'t': straight_data_all['t'], 'straight_data': straight_data_all[str(p)]})
    # straight_data_all[['t', str(p)]] #np.array(straight_data_all)[:,p+1]# straight_data_all[str(p)]

    k = 0
    for i in range(0,len(T)): # for each timelag

        temp = []
        for j in range(0, reps):

            sample = sample_data_timelag2(data = input_data, N = N, T = T[i], seed = None) # new, using timestamps
            norm_data = sample[0]
            lagged_data = sample[1]
            temp = np.append(temp, compute_MI_scalar2(X = norm_data['straight_data'], 
                                                      Y =lagged_data['straight_data'], K=2)) # updated MI Code

        MI_data[:,k] = temp
        k=k+1
        #print(k)
        
    Avg = np.mean(MI_data, axis=0)
    #$print(p)
    return(Avg)


#----- inputs-----
P = np.linspace(0,99,100).astype(int)


# ---- run in parallel -----

worker_num = 24  # how many workers, None means default (max workers)

if __name__ == '__main__':
    
    inputs = P
        
    pool = Pool(worker_num) # gathers pool of workers

    result = pool.map(compute_MI_of_MSSI, P)
    
    
    
#----fit to decay------
def decay(x, a,  b ,c):
    return a*np.exp(-x/b) +c


MI_decay_val = np.zeros((100))

for i in range(0, 100):
    popt, pcov = curve_fit(decay,  np.logspace(-1.5,1,15), result[i]) #T, df[df['test']==i]['MSSI_MI'])
    # plt.plot(T, (decay(T,*popt)))
    MI_decay_val[i] = popt[2]
    
    
    
MI_decay_val = pd.DataFrame(MI_decay_val)
MI_decay_val.to_csv('MI_decay_val_ABP_V6_a.csv')
# straight_data_df.to_csv('straight_data_V6.csv')



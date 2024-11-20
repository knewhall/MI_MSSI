import numpy as np
import pandas as pd 
import scipy
from scipy.spatial import cKDTree
from scipy.special import digamma

# ------- MUTUAL INFORMATION BETWEEN TWO 1-D SCALAR RANDOM VARIABLES -----

def compute_MI_scalar2(X, Y, K):
    '''
    Takes in data as array
    '''
    
    
    K = 2
    # ---- COMPUTE NEAREST NEIGHBOR -----

    L = len(X)
    ni_X = []
    ni_Y = []
    for i in range(0, L):

        # compute subspace dist between ref point and every other point
        d = []
        dist = np.zeros((L,2)) 
        for j in range(0,L):
            temp_x = np.abs(X[i]- X[j])

            temp_y = np.abs(Y[i]- Y[j])

            d.append(max(temp_x,temp_y)) 

            dist[j,:] = [temp_x, temp_y] 

        d = [x for x in d if x > 0] # do not include self

        # record distance to nearest neighbor
        ei = np.min(d) 

        dist_x = dist[:,0] 
        dist_y = dist[:,1] 

        # count neighbors in subspaces
        num_X = len(dist_x[(0 < dist_x) & (dist_x < ei)]) #-1
        num_Y = len(dist_y[(0 < dist_y) & (dist_y < ei)]) #-1 

        ni_X = np.append(ni_X,num_X)
        ni_Y = np.append(ni_Y,num_Y)


    # ---- COMPUTE MUTUAL INFORMATION -----
        # only add 1 to zeros and don't subtract 1
#     for i in range(0, len(ni_X)):
#         if(ni_X[i] == 0 ):
#             ni_X[i]=1

#     for i in range(0, len(ni_Y)):
#         if(ni_Y[i] == 0 ):
#             ni_Y[i]=1

    nx = ni_X + 1 # add self interaction back
    ny = ni_Y + 1

    # use k-1 since we had to K=2 to find nearest neighbor that wasn't self
    I = digamma(K-1) - np.mean(digamma(nx) + digamma(ny)) + digamma(L)
    # print('add 1 only when 0')
    return(I)#,digamma(K-1) ,- np.mean(digamma(nx) + digamma(ny)) , digamma(L), nx, ny)



# ------- MUTUAL INFORMATION BETWEEN TWO 1-D ANGULAR RANDOM VARIABLES -----

#--------ANGLE DISTANCE FUNCTION----------

def angle_distance(cos1, cos2, sin1, sin2):
    temp = cos1*cos2 + sin1*sin2
    if(temp > 1):
        temp = 1
    if(temp < -1):
        temp = -1
    return(np.arccos(temp))

def compute_MI_scalar_angles(data, K):
    '''
    Data must be input as a dataframe containing the cos, sin of each random variable 
    '''
    
    K = 2
    # ---- COMPUTE NEAREST NEIGHBOR -----

    L = len(data)
    cos1 = np.array(data['cos1'])
    cos2 = np.array(data['cos2'])
    sin1 = np.array(data['sin1'])
    sin2 = np.array(data['sin2'])


    ni_X = []
    ni_Y = []
    for i in range(0, L):

        # compute subspace dist between ref point and every other point
        d = []
        dist = np.zeros((L,2)) 
        for j in range(0,L):
            temp_x = angle_distance(cos1[i],cos1[j],
                                    sin1[i], sin1[j])

            temp_y = angle_distance(cos2[i],cos2[j],
                                    sin2[i], sin2[j])

            d.append(max(temp_x,temp_y)) 

            dist[j,:] = [temp_x, temp_y] 

        d = [x for x in d if x > 0] 

        # record distance to nearest neighbor
        ei = np.min(d) 

        dist_x = dist[:,0] 
        dist_y = dist[:,1] 

        # count neighbors in subspaces
        num_X = len(dist_x[(0 < dist_x) & (dist_x < ei)]) #-1
        num_Y = len(dist_y[(0 < dist_y) & (dist_y < ei)]) #-1 

        ni_X = np.append(ni_X,num_X)
        ni_Y = np.append(ni_Y,num_Y)


    # ---- COMPUTE MUTUAL INFORMATION -----
        # only add 1 to zeros and don't subtract 1
#     for i in range(0, len(ni_X)):
#         if(ni_X[i] == 0 ):
#             ni_X[i]=1

#     for i in range(0, len(ni_Y)):
#         if(ni_Y[i] == 0 ):
#             ni_Y[i]=1

    nx = ni_X + 1 # add 1 because digamma(0) = -inf
    ny = ni_Y + 1

    # use k-1 since we had to K=2 to find nearest neighbor that wasn't self
    I = digamma(K-1) - np.mean(digamma(nx) + digamma(ny)) + digamma(L)
    
    return(I)#, digamma(K-1), - np.mean(digamma(nx) + digamma(ny)) , digamma(L), nx, ny)



# ------- MUTUAL INFORMATION BETWEEN ONE 1D SCALAR AND ONE 1D ANGULAR RANDOM VARIABLE -----

def compute_MI_scalar_mixed(angle_data, linear_data, K):
    '''
    Takes in angle data and scalar data as arrays
    '''
    
    K = 2
    # ---- COMPUTE NEAREST NEIGHBOR -----

    L = len(angle_data)
    cos1 = np.array(np.cos(angle_data))
    sin1 = np.array(np.sin(angle_data))

    ni_X = []
    ni_Y = []
    for i in range(0, L):

        # compute subspace dist between ref point and every other point
        d = []
        dist = np.zeros((L,2)) 
        for j in range(0,L):
            temp_x = angle_distance(cos1[i],cos1[j],
                                    sin1[i], sin1[j])

            temp_y = np.abs(linear_data[i]- linear_data[j])

            d.append(max(temp_x,temp_y)) 

            dist[j,:] = [temp_x, temp_y] 

        d = [x for x in d if x > 0] 

        # record distance to nearest neighbor
        ei = np.min(d) 

        dist_x = dist[:,0] 
        dist_y = dist[:,1] 

        # count neighbors in subspaces
        num_X = len(dist_x[(0 < dist_x) & (dist_x < ei)]) #-1
        num_Y = len(dist_y[(0 < dist_y) & (dist_y < ei)]) #-1 

        ni_X = np.append(ni_X,num_X)
        ni_Y = np.append(ni_Y,num_Y)


    # ---- COMPUTE MUTUAL INFORMATION -----
        # only add 1 to zeros and don't subtract 1
#     for i in range(0, len(ni_X)):
#         if(ni_X[i] == 0 ):
#             ni_X[i]=1

#     for i in range(0, len(ni_Y)):
#         if(ni_Y[i] == 0 ):
#             ni_Y[i]=1

    nx = ni_X + 1 # add 1 because digamma(0) = -inf
    ny = ni_Y + 1

    # use k-1 since we had to K=2 to find nearest neighbor that wasn't self
    I = digamma(K-1) - np.mean(digamma(nx) + digamma(ny)) + digamma(L)
    return(I)


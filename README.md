# MI_MSSI
Contained in this directory is the code used to (1) generate particle trajectories of a self-avoidant model droplet (2) compute a straightness index time series to quantify the curvature of the trajectory over a selected course-graining and (3) compute the time-delayed self mutual information of this straightness time series.  

If you use this code, please cite: [K. Daftari and K. Newhall (2024) "Memory signatures in path curvature of self-avoidant model particles are revealed by time delayed self mutual information" 	arXiv:2403.19393](https://arxiv.org/abs/2403.19393)

## (1) run_paths_pool.py
This file generates the trajectory data of the self-avoidant droplet model

It calls functions from Combined_fxns_single_2D.py for the full model or can be changed to call functions from Combined_trunc_fxns_single_2D.py for the truncated time-integral model

## (2) Straightness_Compute.ipynb
This file computes the straightness index time series as the ratio of bird-eye distance to arc length over a specified window size after the data is downsampled by a granularity size

## (3) compute_MI_of_MSSI.py
This file computes the time-delayed self mutual information of the straightness index time series data

It calls the function from the files MI_Functions_Copy.py and Sampling_Timelag_Copy.py





## compute_msd.py
This file computes the mean squared displacement of the trajectory data

## compute_vcf.py
This file computes the velocity correlation function of the trajectory data

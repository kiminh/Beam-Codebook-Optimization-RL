# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:55:17 2019

@author: (Ethan) Yuqiang Heng
"""
import numpy as np
from typing import Tuple


#time_factor = 20
#cov_factor = 5
#default_means = np.array([[640,470],[600,460],[680,460],[640,400]])
#bs_loc = [641,435]
#default_covs = np.array([[[cov_factor,0],[0,cov_factor]] for i in default_means])
#default_arr_rates = np.array([time_factor for i in default_means])
h_imag_fname = "H_Matrices FineGrid/MISO_Static_FineGrid_Hmatrices_imag.npy"
h_real_fname = "H_Matrices FineGrid/MISO_Static_FineGrid_Hmatrices_real.npy"
ue_loc_fname = "H_Matrices FineGrid/MISO_Static_FineGrid_UE_location.npy"
bs_loc = [641,435,10]
n_antenna = 64

class GaussianCenters():
    def __init__(self, 
#               means:np.array=default_means, #2-d array w/. shape lx2, l centers
#               covs:np.array=default_covs, #3-d array w/. shape lx2x2, covariance of each center
#               arrival_rates:np.array=default_arr_rates # 1-d lx1 array, arrival rates of UEs at each center
               n_clusters = 4, arrival_rate = 5, cluster_variance = 5
               ):
        self.arrival_rate = arrival_rate
        self.cluster_variance = cluster_variance
#        assert means.shape[1] == covs.shape[1] == covs.shape[2] == 2
#        assert means.shape[0] == covs.shape[0] == arrival_rates.shape[0]
        default_means = np.array([[640,470],[600,460],[680,460],[640,400]])
        bs_loc = [641,435]
        default_covs = np.array([[[self.cluster_variance,0],[0,self.cluster_variance]] for i in default_means])
        default_arr_rates = np.array([arrival_rate for i in default_means])
        self.means = default_means
        self.covs = default_covs
        self.arrival_rates = default_arr_rates
        self.n_cluster = n_clusters
        
    def sample(self) -> Tuple[int, np.array]:
        """
        output:
            n x 2 array, coordinates of n UEs generated according to arrival rates and centers
            assuming poisson arrival at each center
        """
#        num_UEs = np.random.poisson(lam = self.arrival_rates).astype(int)
        num_UEs = np.random.randint(0,self.arrival_rate*2,len(self.arrival_rates)) #uniform arrival rate so that its bounded
        total_num_UEs = sum(num_UEs)
        all_samples = np.zeros((total_num_UEs,2))
        for i in range(self.arrival_rates.shape[0]):
            samples = np.random.multivariate_normal(self.means[i,:], self.covs[i,:,:], num_UEs[i])
            all_samples[sum(num_UEs[0:i]):sum(num_UEs[0:i+1]),:] = samples
        return total_num_UEs, all_samples
    
        
    
class Uniform_UE():
    """
    Uniform type arrival process: x, y coordinates are drawn from uniform dist., num arrivals drawn from uniform dist.
    """
    def __init__(self, tot_num_pts:int = 58725, arrival_rate = 5):
        self.arrival_rate = arrival_rate
        self.tot_num_pts = tot_num_pts
    
    def sample(self) -> Tuple[int, np.array]:
        num_sample = np.random.randint(0, self.arrival_rate*2)
        return num_sample, np.random.choice(self.tot_num_pts, num_sample, replace = False)
    
class BirthDeathGaussianCenters():
    def __init__(self, 
#               means:np.array=default_means, #2-d array w/. shape lx2, l centers
#               covs:np.array=default_covs, #3-d array w/. shape lx2x2, covariance of each center
#               arrival_rates:np.array=default_arr_rates # 1-d lx1 array, arrival rates of UEs at each center
               n_clusters: int = 4, arrival_rate = 5, cluster_variance = 5, tot_num_pts:int = 58725,
               ):
        self.arrival_rate = arrival_rate
        self.cluster_variance = cluster_variance
        self.tot_num_pts = tot_num_pts
#        assert means.shape[1] == covs.shape[1] == covs.shape[2] == 2
#        assert means.shape[0] == covs.shape[0] == arrival_rates.shape[0]
        default_means = np.array([[640,470],[600,460],[680,460],[640,400]])
        bs_loc = [641,435]
        default_covs = np.array([[[self.cluster_variance,0],[0,self.cluster_variance]] for i in default_means])
        default_arr_rates = np.array([arrival_rate for i in default_means])
        self.means = default_means
        self.covs = default_covs
        self.arrival_rates = default_arr_rates
        self.n_clusters = n_clusters
        self.all_loc = np.load(ue_loc_fname)[:,0:2]
        
    def gen_new_clusters(self):
        new_cluster_centers = np.zeros((self.n_clusters,2))
        for cluster_idx in range(self.n_clusters):       
            if cluster_idx == 0:
                sample_loc_idx = np.random.choice(self.tot_num_pts)
                sample_loc = self.all_loc[sample_loc_idx]     
                new_cluster_centers[cluster_idx,:] = sample_loc
            else:
                while True:
                    sample_loc_idx = np.random.choice(self.tot_num_pts)
                    sample_loc = self.all_loc[sample_loc_idx]    
                    min_dist = min(np.linalg.norm(new_cluster_centers[0:cluster_idx-1,:] - sample_loc, axis=1))
                    if min_dist > 2*self.cluster_variance:
                        new_cluster_centers[cluster_idx,:] = sample_loc
                        break
        return new_cluster_centers 
                     

    
#class TimeVaryingGaussianCenters():
#    def __init__(self, 
#               arrival_rate = 5, cluster_variance = 5, num_clusters = 5
#               ):    
#        self.arrival_rate = arrival_rate
#        self.cluster_variance = cluster_variance 
#        self.t = 0
        
        
if __name__ == "__main__":
    gc = GaussianCenters()
    for i in range(5):
        print(gc.sample()[1].shape)
        


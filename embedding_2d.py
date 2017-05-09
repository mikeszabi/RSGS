# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:46:39 2017

@author: SzMike
"""


import numpy as np
from matplotlib import pyplot as plt
#import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

from sklearn import manifold
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

#%matplotlib qt5

def normalize_coordinates(Y):
    Y-= np.min(Y,axis=0)
    Y/= np.max(Y,axis=0)

    return Y

def make_granular(Y,granularity):
    Y*=granularity
    Y=np.floor(Y).astype('uint8')
    return Y

def t_sne(features,granularity_scale,vis_diag=True):

    feat_list=[np.asarray(feat) for feat in features.values()]

    feat_array=np.asarray(feat_list)
    
  
    model = manifold.TSNE(n_components=2, random_state=0, \
                      perplexity=10, learning_rate=100, n_iter=10000, \
                      init='pca',\
                      metric='cosine')
    Y=model.fit_transform(feat_array) 

    Y=normalize_coordinates(Y)
    
    if vis_diag:

        fig=plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
        ax.axis('tight')
        ax.grid(True)                                                
        plt.show()
        
    Y=make_granular(Y,granularity_scale)
    
    clust_id=[]
    for coordinates in Y:
        clust_id.append(str(int(coordinates[0]))+'_'+str(int(coordinates[1])))
    return clust_id

def k_means(features,n_clusters,vis_diag=True):
    
    feat_list=[np.asarray(feat) for feat in features.values()]

    feat_array=np.asarray(feat_list)
    
    pca = PCA(n_components=25)
    pca_feat_array = pca.fit_transform(feat_array)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(pca_feat_array)
    
    clust_id=[]
    for labels in kmeans.labels_:
        clust_id.append(str(labels))
    
    return clust_id
    
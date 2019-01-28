# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 15:46:39 2017

@author: SzMike
"""

import sys
import time
import file_helper
import os
import json
import numpy as np
from matplotlib import pyplot as plt
import cnn_feature_service
import matplotlib.gridspec as gridspec
from matplotlib.ticker import NullFormatter
import matplotlib.patches as patches
import matplotlib.cm as cmx
import matplotlib.colors as colors

from sklearn import manifold
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from PIL import Image

import image_scatter

%matplotlib qt5



def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color

def normalize_coordinates(Y):
    Y-= np.min(Y,axis=0)
    Y/= np.max(Y,axis=0)

    return Y
def make_granular(Y,granularity):
    Y*=granularity
    Y=np.floor(Y).astype('uint8')
    return Y

onedrive_use='SzMike'

granularity=6

#base_folder = r'd:\Projects\WISH'
base_folder = os.path.curdir
feature_file=r'd:\DATA\RealEstate\784730\features.json'

features=cnn_feature_service.load_db_features(feature_file)

images=[]
for im in features.keys():
    print(im)
    imgobj=Image.open(im)
    imgobj.thumbnail((200,200), Image.ANTIALIAS)
    images.append(np.array(imgobj))

feat_list=[np.asarray(feat) for feat in features.values()]

feat_array=np.asarray(feat_list)
pca = PCA(n_components=20)
pca_feat_array = pca.fit_transform(feat_array)
    
model = manifold.TSNE(n_components=2, random_state=0, \
                      perplexity=10, learning_rate=100, n_iter=10000, \
                      init='pca',\
                      metric='cosine')
# metrics: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
Y=model.fit_transform(pca_feat_array) 

Y=normalize_coordinates(Y)

canv,centers=image_scatter.image_scatter(Y, images, 200, res=4000, cval=2.)


kmeans = KMeans(n_clusters=granularity, random_state=0).fit(pca_feat_array)
kmeans.labels_


"""
"""

fig=plt.figure()
ax = fig.add_axes([0,0,1,1])

sp=np.linspace(0,1,granularity+1)
for x in sp[:-1]:
    for y in sp[:-1]:        
        p = patches.Rectangle(
                (x, y), 1/granularity, 1/granularity,
                fill=False, color='red', alpha=0.2, transform=ax.transAxes, clip_on=False
                )
    
        ax.add_patch(p)

plt.scatter(Y[:, 1], 1-Y[:, 0], cmap=plt.cm.Spectral)
plt.axis('tight')
ax = fig.gca()
for i, pts in enumerate(Y):
    ax.text(Y[i, 1],1-Y[i, 0],str(kmeans.labels_[i]),color='red', fontsize=15)

plt.show()

#Y=make_granular(Y,4)

"""
"""
cmap = get_cmap(granularity*granularity)

sp_x=np.linspace(0,canv.shape[1],granularity+1)
sp_y=np.linspace(0,canv.shape[0],granularity+1)




fig=plt.figure()

#ax.set_xticks(np.arange(0, canv.shape[0], canv.shape[0]/3))
#ax.set_yticks(np.arange(0, canv.shape[1], canv.shape[1]/3))
#ax.grid(True)
ax = fig.add_axes([0,0,1,1])
for x in sp_x[:-1]:
    for y in sp_y[:-1]:        
        p = patches.Rectangle(
                (x, y), canv.shape[1]/granularity, canv.shape[0]/granularity,
                fill=False, edgecolor='red', alpha=0.3, transform=ax.transAxes, clip_on=False
                )
        ax.add_patch(p)

ax.imshow(canv)
for i, pts in enumerate(centers):
    ax.text(pts[1],pts[0],str(kmeans.labels_[i]),color='red', backgroundcolor='white', fontsize=10)



plt.show()
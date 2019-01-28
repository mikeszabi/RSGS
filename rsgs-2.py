# -*- coding: utf-8 -*-
"""
Created on Tue May  2 14:59:18 2017

@author: SzMike
"""

import sys, math, os
import numpy as np
import tkinter as tk
from tkinter.filedialog import SaveAs, Directory
from collections import OrderedDict
from PIL import Image                                  # PIL Image: also in Tkinter
from PIL.ImageTk import PhotoImage                # PIL photo widget replacement

import image_views  
import file_helper
import cnn_feature_service
import aes_AADB_opencv as aes
import json

import embedding_2d
import cfg
        

# remember last dirs across all windows
openDialog = Directory(title='Select Image Directory To Open')
appname = 'RSG 1.0: '
base_folder = os.path.curdir

class image_set:
    def __init__(self):
        self.current_dir=''
        self.image_list=[]
        self.image_scores={}
        self.features=[]
        self.clust_coordinates=[]
#        self.group_coordinates=[]
        self.image_group_ids={}
        self.group_ids={}
        self.group_represent={}
        
        self.is_Features_ready=False
        self.is_Scores_ready=False
        self.scoring=aes.scoring()

        model_type='ResNet_18'
        self.param=cfg.param(model_type)
        self.image_list_file, feature_file, model_file = self.param.getDirs(base_folder=base_folder)
        
        self.cnf=cnn_feature_service.cnn_features(self.param,model_file)    
        
    def new_list(self,image_dir):
        self.current_dir=image_dir
        self.image_list=file_helper.imagelist_in_depth(image_dir,level=0)
        self.is_Features_ready=False
        self.is_Scores_ready=False
        self.image_label={}
        for i,image in enumerate(self.image_list):
            self.image_label[image]=0
#        with open(self.image_list_file, 'w') as imagelistfile:
#                json.dump(self.image_list,imagelistfile)
#        
    def create_image_score(self):
        if self.image_list and (not self.is_Scores_ready):
            image_score_file=os.path.join(self.current_dir,'scores.json')
            self.is_Scores_ready=True
            if os.path.exists(image_score_file):
                with open(image_score_file, 'r') as fp:
                    im_scores = json.load(fp)
            else:
                # Get the scores
                image_all_scores=self.scoring.get_scores(self.image_list)
                im_scores={}
                for i,image in enumerate(self.image_list):
                   im_scores[image]=image_all_scores[i]['AestheticScore']
                with open(image_score_file, 'w') as fp:
                    json.dump(im_scores,fp)
            self.image_scores=OrderedDict(sorted(im_scores.items(), key=lambda t: t[1], reverse=True))
        print('...Scores are ready')
            
                
    def create_features(self):
        if self.image_list and (not self.is_Features_ready):  
            image_feature_file=os.path.join(self.current_dir,'features.json')
            self.is_Features_ready=True
            if os.path.exists(image_feature_file):
                with open(image_feature_file, 'r') as fp:
                    self.features = json.load(fp)
            else:
                self.features=self.cnf.create_cnn_features(self.image_list)
            with open(image_feature_file, 'w') as fp:
                json.dump(self.features,fp)
        print('...Features are ready')
            
    def create_groups(self,granularity_scale):
        if self.image_list and self.features and self.is_Features_ready:              
            self.clust_id=embedding_2d.k_means(self.features,granularity_scale)
            self.image_group_ids={}
            for i,images in enumerate(list(self.features.keys())):
                self.image_group_ids[images]=self.clust_id[i]
            self.group_ids=np.unique(list(self.image_group_ids.values()))                                  
            self.group_represent={}
            for id in self.group_ids:
                group_items = {key : self.image_scores[key] for key, val in self.image_group_ids.items() if val==id}
                group_items=OrderedDict(sorted(group_items.items(), key=lambda t: t[1], reverse=True))
                self.group_represent[next(iter(group_items.items()))[0]]=group_items
#             type(list(imset.group_represent.values())[0])==OrderedDict  


class rsgs(tk.Frame):
    def __init__(self, master,imset):
        self.imset=imset
        
        tk.Frame.__init__(self, master, background="green")
        tk.Button(self, text='Open Image Directory', command=self.onDirectoryOpen).pack( )
        tk.Button(self, text='Get Scores', command=self.onScoring).pack( )
        tk.Button(self, text='Create Features', command=self.onCreateFeat).pack( )
        tk.Button(self, text='Grouping', command=self.onGrouping).pack( )
        
        self.granularity_scale=tk.Scale(self,from_=1, to=50, orient=tk.HORIZONTAL)
        self.granularity_scale.pack()
        self.granularity_scale.set(10)
        
    def onDirectoryOpen(self):
        """
        open a new image directory in new pop up
        available in both thumb and img windows
        """
        image_dir = openDialog.show( )
        
        if image_dir:
            self.imset.new_list(image_dir)
            #set_id='thumbs'
            #image_views.viewThumbs(self.imset.image_scores, set_id, kind=tk.Toplevel)
        
    def onCreateFeat(self):
        """
        creating features
        """
        self.imset.create_features()

    def onScoring(self):
        """
        creating scores
        """
        self.imset.create_image_score()
        if self.imset.image_scores:
            set_id='thumbs'
            image_views.viewThumbs(self.imset.image_scores, set_id, kind=tk.Toplevel)
        
    def onGrouping(self):
        """
        creating features
        """
        self.imset.create_groups(self.granularity_scale.get())
        if self.imset.group_represent:
            set_id='represent'
            image_views.viewThumbs(self.imset.group_represent, set_id, kind=tk.Toplevel)
    
if __name__ == '__main__':

    imset=image_set()
    
    root = tk.Tk()
    root.title(appname + 'Open')
    rsgs_w=rsgs(root,imset)
    rsgs_w.pack(fill="both", expand=True)
   
    root.mainloop( )
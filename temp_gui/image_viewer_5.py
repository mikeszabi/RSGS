# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 14:02:45 2017

@author: SzMike
"""


import tkinter as tk
import numpy as np
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk

import object_detection


user='SzMike' # picturio


class ImageViewer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, background="green")
        

        browse_button = tk.Button(self, text="Browse", command=self.load_file, width=10)
        browse_button.grid(row=0, column=0, sticky=tk.W)
        #find_button = tk.Button(self, text="Find Similar", command=self.find_similar, width=10)
        #find_button.grid(row=0, column=1, sticky=tk.W)
       
        self.query_im = Image.open(r'd:\DATA\RealEstate\117600\10026.jpg')
        self.query_im.thumbnail((200,200))
        self.query_img = ImageTk.PhotoImage(self.query_im)
        self.q2_im = None
        self.q2_img = None
        self.query_panel = None
        self.q2_panel = None
        self.query_panel = tk.Label(self, image = self.query_img)
        self.query_panel.grid(row=1,column=0)
        
        self.query_panel_2 = tk.Label(self, image = self.query_img)
        self.query_panel_2.grid(row=2,column=0)
        
        self.query_panel_3 = tk.Label(self, image = self.query_img)
        self.query_panel_3.grid(row=1,column=1)
        
        self.query_panel_4 = tk.Label(self, image = self.query_img)
        self.query_panel_4.grid(row=2,column=1)

#        for i in range(self.top_count):
#            self.sim_im[i] = None
#            self.sim_img[i] = None
#            self.sim_panel[i] = tk.Label(self, image = self.sim_img[i])
#            self.sim_panel[i].grid(row=1,column=i+1)
        
    def load_file(self):
        query_path = askdirectory()
        

#        for i in range(self.top_count):
#            self.sim_im[i] = Image.open(query_path)
#            self.sim_im[i].thumbnail((100,100))
#            self.sim_img[i] = ImageTk.PhotoImage(self.sim_im[i])
#            self.sim_panel[i] = tk.Label(self, image = self.sim_img[i])
#            self.sim_panel[i].grid(row=1+i,column=1)
        
#    def find_similar(self):
#      
#        print('...creating cnn features for query image')
#        query_feat=np.array(self.cnn_f.create_feature(self.query_im))
#        cf=self.cnn_f.compare_feature(query_feat.reshape(1,-1),cnn_f.db_features)
#        
#        result_indices = np.argsort(cf)[0,0:3]
#        
#        for i in range(self.top_count):
#            image_file=cnn_f.db_files_list[result_indices[i]]
#            image_file=image_file.replace('picturio',user)
#            self.sim_im[i] = Image.open(image_file)
#            self.sim_im[i].thumbnail((200,200))
#            self.sim_img[i] = ImageTk.PhotoImage(self.sim_im[i])
#            self.sim_panel[i] = tk.Label(self, image = self.sim_img[i], \
#                          text=str(cf[0,result_indices[i]]),\
#                                  compound=tk.BOTTOM)
#            self.sim_panel[i].grid(row=1+i,column=1)

if __name__ == "__main__":
    root = tk.Tk()
    
   # cnn_f=cnn_feature_service.cnn_db_features()
    
    im_w=ImageViewer(root)
    im_w.pack(fill="both", expand=True)
    root.mainloop()
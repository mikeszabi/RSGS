# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:27:39 2017

@author: SzMike
"""

import sys
import os

images=os.listdir(r'D:\Projects\3rdParty\IPOL\ace_20121029\bin\images')

cd D:\Projects\3rdParty\IPOL

for image in images:

    os.system('ace -a 8 -m interp:12 .\\images\\'+image+' .\\enhanced\\enhanced_'+image)
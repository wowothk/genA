#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 09:58:18 2019

@author: rudi
"""
import numpy as np
import pandas as pd
data_Path = '/home/rudi/Documents/import_excel/hasil2.xlsx'


data = pd.read_excel(data_Path,sheet_name='Sheet1')

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


fig3 = plt.figure()
ax3 = fig3.add_axes([0,0,1,1])
ax3.scatter(data['f1'],data['f3'])
plt.show();
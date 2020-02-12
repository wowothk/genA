#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 03:44:22 2020

@author: rudi
"""

import pandas as pd
import numpy as np

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

path='/home/rudi/Documents/import_excel/selangseratus2.xlsx'
#path ='/home/rudi/Documents/skripsi/gen22.xlsx'
df = pd.read_excel(path)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='2d')
#ax.scatter(df['f1'],df['f2'])
#fig.savefig('test.png')

plt.scatter(df['f1'],df['f2'], label="solusi optimal", color='r', s=15, marker="o")

plt.xlabel('f1')
plt.ylabel('f2')
plt.title('Grafik Optimal Pareto')
plt.legend()
plt.show()
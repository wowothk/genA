#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 15:52:18 2019

@author: rudi

program untuk menggenerate populasi
"""

import numpy as np
import random
from repair import repair_alg
from cari_f import create_f
from cari_f import create_b
from susahnya_stage2 import create

def create_populasi(banyak_populasi, supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc):
    """
    dengan supplier, plant,dc, customer merupakan himpunan dalam bentuk string
    
    """
    populasi=[None]*banyak_populasi
    
    for i in range(banyak_populasi):
        create_individu = list(create(supplier, plant, dc, customer, S, K, J,I, maks_plant, maks_dc).supplier_to_plant())
        populasi[i]= create_individu[0:3]
    
    
    return populasi


supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

populasi = create_populasi(5, supplier, plant, dc, customer, sups, D, W, d, 2, 2)

for i in range(len(populasi)):
    print(populasi[i])
    print("++++++++++++++")
    

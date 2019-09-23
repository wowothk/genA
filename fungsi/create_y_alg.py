#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 18:43:57 2019

@author: rudi
fungsi untuk menentukan pasangan yang dc untuk suatu customer
a1 : self.I
a2 : self.dc
b : temp_j
#c : temp_d
d : y
e : z

"""
import random
import numpy as np
def define_y(a1,a2, b, d, e):
    temp_j = [0]*len(b)
    temp_d = [0]*len(a1)
    y = np.array([[0]*len(a1)]*len(b))
    z = [0]*len(b)
    for j in range(len(b)):
        temp_j[j] = b[j]
        z[j] = e[j]
    for i in range(len(a1)):
        temp_d[i] = a1[i]
        
    for j in range(len(b)):
        for i in range(len(a1)):
            y[j][i] = d[j][i]
    
    for x in range(len(a1)):
        print("####iterasi   ", x, "########")
        r = random.randint(0, len(temp_j)-1)
                
        condition= True
        l=0
        temp_random = []
        temp_random_j = []
        while  condition:
            l=l+1
            print('l  ',l)
    #               print('nilai r ', r)
            if z[r] == 1 :
                y[r][x] = 1
            temp_j[r] = temp_j[r] - a1[x]*y[r][x]
            temp_d[x] = temp_d[x] - a1[x]*y[r][x]
            print('r  ',  r,' dan y[r][x] = ', y[r][x])
            print('temp_j[r] =  ', temp_j[r])
            print('temp_d[x] =   ', temp_d[x])
            print('z[r]  ',z[r] )
            print('total j ', sum(np.multiply(temp_j, z)))
            print('total permintaan ', sum(temp_d))
            if l == 50 : break
            if sum(np.multiply(temp_j, z)) < sum(temp_d) or temp_j[r] < 0 or temp_d[r] < 0 or z[r] == 0:
                temp_d[x] = temp_d[x] + a1[x]*y[r][x]
                temp_j[r] = temp_j[r] + a1[x]*y[r][x]
                y[r][x] = 0
#                temp_random_j.append(a2[r])
#                print('temp_random_j  ', temp_random_j)
#                print('apa namnanya  ',set(a2)- set(temp_random_j))
#                if len(temp_random_j)!=0 and len(set(a2)- set(temp_random_j)) == 0:
#                    return
#                else:
#                    r = random.randint(0, len(temp_j)-1) 
            else:
                break       
            
        return y
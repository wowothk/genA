#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 01:03:07 2019

@author: rudi

untuk menentukan f (random)

syaratnya harus dipastikan bahwa total capacity >= total demand
"""
import numpy as np
import random

def create_f(source, depot, cap, dem, p, z, q ):
    '''
    source & depot sebagai himpunan,
    cap & dem sebagai value dari himpunan,
    p :source yang buka mana
    z :depot yang buka mana
    q : banyaknya barang yg dikirim
    '''
#    g[k][j] = min(temp_a[k], temp_b[j])
#        temp_a[k] = temp_a[k]-g[k][j]
#        temp_d[k] = temp_d[k]+g[k][j]
    f = np.array([[0]*len(dem)]*len(cap))
    
    tot_dem_j = [0]*len(dem) # total demand pada setiap depot j
    for  j in range(len(dem)):
        tot_dem_j[j]=sum(q[j])
    Op =[]
#    Cp =[]
    Od =[]
#    Cd =[]
    temp_cap = [0]*len(source)
    temp_dem = [0]*len(depot)
    for k in range(len(source)):
        temp_cap[k] = cap[k]*p[k]
        if p[k] != 0:
            Op.append(source[k])
    for j in range(len(depot)):
        temp_dem[j] = dem[j]
        if z[j] != 0:
            Od.append(depot[j])
#    print('op  ',Op)
#    print('od  ',Od)
#    print(tot_dem_j)
#    print(temp_cap)
#    print('temp_dem   ',tot_dem_j)
    k=0
    i=0
#    while k < len(Op) and len(Od) != 0:
    while sum(tot_dem_j) !=0 and len(Od) !=0:
        i=i+1
#        print('iterasi  ######################',i)
#        if len(Od) != 0:
        rand_k = random.randint(0,len(Op)-1)
        rand_j = random.randint(0,len(Od)-1)
#        print('len od   ', len(Od))
#        print('random   j', rand_j)
#        print('random   k', rand_k)
#        print('Op',Op[k])
#        print('apa ya hehe',source.index(Op[k]))
#        print("lah  ", depot.index(Od[rand_j]))
#        print('op  ',Op)
#        print('od  ',Od)
#        print('depot  ', depot)
        f[source.index(Op[rand_k])][depot.index(Od[rand_j])] = min(temp_cap[source.index(Op[rand_k])],tot_dem_j[depot.index(Od[rand_j])])
        temp_cap[source.index(Op[rand_k])] = temp_cap[source.index(Op[rand_k])] - f[source.index(Op[rand_k])][depot.index(Od[rand_j])]
        tot_dem_j[depot.index(Od[rand_j])] = tot_dem_j[depot.index(Od[rand_j])] - f[source.index(Op[rand_k])][depot.index(Od[rand_j])]
#        print(temp_dem[depot.index(Od[rand])])
        if temp_cap[source.index(Op[rand_k])] == 0:
            Op.remove(Op[rand_k])
#            k =0
#            print('haiiii  ')
#        else:
#            k=k+1
#        print(len(Op))
        if tot_dem_j[depot.index(Od[rand_j])] == 0:
            Od.remove(Od[rand_j])
#        print(len(Od), Od)
#        print(tot_dem_j)
#        print(temp_cap)
#    print('nilai ep  ', f)
    return f

def create_b(source, depot, cap, dem, p, f):
    b = np.array([[0]*len(dem)]*len(cap))
    
    tot_dem_k = [0]*len(dem) # total demand pada setiap depot j
    for  k in range(len(dem)):
        tot_dem_k[k]=sum(f[k])
    temp_source =[None]*len(source)
    Op =[]
    temp_cap = [0]*len(source)
    temp_dem = [0]*len(depot)
    for s in range(len(source)):
        temp_cap[s] = cap[s]
        temp_source[s] = source[s]
#    print('p  ', p)
    for k in range(len(depot)):
        temp_dem[k] = dem[k]*p[k]
        if p[k] != 0:
            Op.append(depot[k])
#    print('source  ', source)
#    print('depot   ', depot)
#    print('banyak permintaan  ', tot_dem_k)
#    print('kapasitas  ', temp_cap)
#    while k < len(Op) and len(Od) != 0:
    i=0
    while sum(tot_dem_k) !=0 and len(Op) !=0:
        i=i+1
#        print('iterasi  ######################',i)
#        print('Op  ', Op)
        rand_k = random.randint(0,len(Op)-1)
        rand_s = random.randint(0,len(temp_source)-1)
#        print('rand_k   ',rand_k)
#        print('rand_s   ', rand_s)
#        print('nilai minimum     ', min(temp_cap[source.index(temp_source[rand_s])],tot_dem_k[depot.index(Op[rand_k])]))
#        print('temp_source  ', temp_source[rand_s])
#        print('temp_source  ', source.index(temp_source[rand_s]))
        b[source.index(temp_source[rand_s])][depot.index(Op[rand_k])] = min(temp_cap[source.index(temp_source[rand_s])],tot_dem_k[depot.index(Op[rand_k])])
        temp_cap[source.index(temp_source[rand_s])] = temp_cap[source.index(temp_source[rand_s])] - b[source.index(temp_source[rand_s])][depot.index(Op[rand_k])]
        tot_dem_k[depot.index(Op[rand_k])] = tot_dem_k[depot.index(Op[rand_k])] - b[source.index(temp_source[rand_s])][depot.index(Op[rand_k])]
#        print(temp_dem[depot.index(Od[rand])])
        if temp_cap[source.index(temp_source[rand_s])] == 0:
            temp_source.remove(temp_source[rand_s])

        if tot_dem_k[depot.index(Op[rand_k])] == 0:
            Op.remove(Op[rand_k])
#        print(len(Od), Od)
#        print(tot_dem_k)
#        print(temp_cap)
        if i == 20:
            break
    return b
    
#supplier = ["s1","s2","s3"]
#plant = ["p1","p2","p3"]
#dc = ["dc1","dc2","dc3","dc4"]
#customer =["cust1","cust2", "cust3","cust4"]
#
#sups =[250,200,250]
#D = [200,150,200] 
#W = [150, 100, 200, 100]
#d = [50, 100, 50, 100]
#
#p = [0,1,1]
#z= [1,0,1,0]
#q= np.array([[50,100,0,0],[0,0,0,0],[0,0,50,100],[0,0,0,0]])
#f=np.array([[0,0,0,0],[0,0,150,0],[150,0,0,0]])
##print(create_f(plant, dc, D, W,p,z,q))
##print("aku rapaham")
##print(q)
#
#print(create_b(supplier, plant, sups, D, p, f))
#print("==============================")
#print(f)
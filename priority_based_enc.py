#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:49:26 2019

@author: rudi

"""
import random
class priority_based_enc:
    def __init__(self, sources, depot, a, b, c, g):
        self.sources = sources
        self.depot = depot
        self.a = a
        self.b = b
        self.c = c
        self.g = g
    """
    dengan 
    sources: himpunan sumber; depot: himpunan tujuan;
    a: kapasitas sumber; b: kapasitas tujuan;
    c: matrik biaya; g: banyaknya yang dikirim dari sources k ke depot j
    """
    def encoding(self):
        temp_sources = self.a.copy()
        temp_depot= self.b.copy()
        v = [None]*(len(self.depot)+len(self.sources))
        p = len(self.depot)+len(self.sources)
#        i=0
        index=[0,0]
        while temp_depot[index[1]] != 0 or temp_sources[index[0]] != 0:
            temp_c = 0 
#            print("=========================")
            was_passed = False
            for k in range(len(self.sources)):
#                print('k',k)
#                print('++++++++++++++++++')
                for j in range(len(self.depot)):
#                    print('j  ',j)
#                    print('temp_sources', temp_sources[k])
#                    print('temp_depot',  temp_depot[j])
#                    print('g[k][j]', self.g[k][j])
                    if self.g[k][j] != 0 and (temp_depot[j] == self.g[k][j] or temp_sources[k]==self.g[k][j]):
                        if temp_c == 0 and was_passed == False:
                            temp_c=self.c[k][j]
                            index[0] = k
                            index[1] = j
                            was_passed = True
#                            print('lewat sini',k,j)
                        elif self.c[k][j] < temp_c:
                            temp_c = self.c[k][j]
                            index[0] = k
                            index[1] = j
#                print(index)
#            break
            temp_depot[index[1]] = temp_depot[index[1]]-self.g[index[0]][index[1]]
            temp_sources[index[0]] = temp_sources[index[0]]-self.g[index[0]][index[1]]                
            if temp_depot[index[1]] == 0 :
                v[len(self.sources)+index[1]] = p 
                p = p-1
                self.g[index[0]][index[1]] = 0
            if  temp_sources[index[0]] == 0 :
                v[index[0]] = p 
                p = p-1
                self.g[index[0]][index[1]] = 0
        return v
    
supplier = ["s1","s2","s3"]
#plant = ["p1","p2","p3"]
plant1 = ["p1","p2","p3",'dummy']
#dc = ["dc1","dc2","dc3","dc4"]
#customer =["cust1","cust2", "cust3","cust4"]
#
#import numpy as np
#sups =[250,200,250]
#D = [200,150,200] 
#D1 = [200,100,0,400] 
#W = [150, 100, 200, 100]
#d = [50, 100, 50, 100]
#
#b = np.array([[0,150,100],[0,0,0],[0,0,50]]) 
#b1 = np.array([[50,0,0,200],[0,0,0,200],[150,100,0,0]]) 
#f = np.array([[0,0,0,0],[0,0,150,0],[150,0,0,0]])
#q = np.array([[50,100,0,0],[0,0,0,0],[0,0,50,100],[0,0,0,0]])
#
#t = np.array([[4,3,1],[3,5,2],[1,6,4]])
#t1 = np.array([[4,3,1,0],[3,5,2,0],[1,6,4,0]])
#a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
#c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
#
#stage1 = priority_based_enc(supplier, plant1, sups, D1, t1, b1)
#v1 = stage1.encoding()
#print(v1)
        

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]
import numpy as np
t = np.array([[4,3,1],[3,5,2],[1,6,4]])
t1 = np.array([[4,3,1,0],[3,5,2,0],[1,6,4,0]])
a = np.array([[5,2,4,3],[4,6,3,5],[3,5,1,6]])
c = np.array([[3,5,2,4],[6,2,5,1],[4,3,6,5],[2,4,3,2]])
individu=[(np.array([[ 50,   0,   0],
         [  0,   0,   0],
         [150, 100,   0]]), np.array([[  0,   0, 200,   0],
         [  0,   0,   0, 100],
         [  0,   0,   0,   0]]), np.array([[  0,   0,   0,   0],
         [  0,   0,   0,   0],
         [ 50, 100,  50,   0],
         [  0,   0,   0, 100]]), [1, 1, 0], np.array([0, 0, 1, 1]))]

#chromosom = enc_pop(individu, supplier, plant, dc, customer, sups, D, W, d, t, a, c)
#print(chromosom)
#decode_chromosom = stage_1(supplier, plant, dc, customer, 1, sups, D, W, d, chromosom[0][0],chromosom[0][1],chromosom[0][2], t, a).decode()
#print(decode_chromosom)

temp=[[ 50,   0,   0],
         [  0,   0,   0],
         [150, 100,   0]]
temp1=[[ 50,   0,   0,200],
         [  0,   0,   0,200],
         [150, 100,   0,0]]
pengkodean = priority_based_enc(supplier, plant1, sups,[200,100,0,400],t1,temp1).encoding()
print(pengkodean)
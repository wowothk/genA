#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:49:26 2019

@author: rudi

"""

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
        temp_sources = [None]*len(self.sources)
        temp_depot= [None]*len(self.depot)
        for k in range(len(self.sources)):
            temp_sources[k] = self.a[k]
    
        for j in range(len(self.depot)):
            temp_depot[j]=self.b[j]
    
        v = [None]*(len(self.depot)+len(self.sources))
        p = len(self.depot)+len(self.sources)
#        i=0
        index=[0,0]
        while temp_depot[index[1]] != 0 or temp_sources[index[0]] != 0:
            temp_c = 0 
            for k in range(len(self.sources)):
                for j in range(len(self.depot)):
                    if self.g[k][j] != 0 and (temp_depot[j] == self.g[k][j] or temp_sources[k]==self.g[k][j]):
                        if temp_c == 0:
                            temp_c=self.c[k][j]
                            index[0] = k
                            index[1] = j
                        elif self.c[k][j] < temp_c:
                            temp_c = self.c[k][j]
                            index[0] = k
                            index[1] = j
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
    
    
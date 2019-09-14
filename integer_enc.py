#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:13:35 2019

@author: rudi
"""

class integer_encoding:
    def __init__(self, sources, depot, a, b, c, q):
        self.sources = sources
        self.depot = depot
        self.a = a
        self.b = b
        self.c = c
        self.q = q
    
    """
    dengan 
    sources: himpunan sumber; depot: himpunan tujuan;
    a: kapasitas sumber; b: kapasitas tujuan;
    c: matrik biaya; q: banyaknya yang dikirim dari sources k ke depot j
    """
    def encode(self):
        v = [0]*len(self.depot)
        for j in range(len(self.sources)):
            for i in range(len(self.depot)):
                if self.q[j][i] != 0:
                    v[i] = j+1
        
        return v

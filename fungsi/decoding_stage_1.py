#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 01:00:10 2019

@author: rudi

decoding stage 1

"""
import numpy as np
from prosedur1 import decoding
class stage_1:
    def __init__(self, S, K, D_aksen, t, u, a, v1):
        self.S = S
        self.K = K
        self.D_aksen = D_aksen
        self.t = t
        self.u = u 
        self.a = a
        self.v1 =v1
    def decode(self):
        b = np.array([[0]*self.S]*self.K)
        for k in range(len(self.K)):
            self.a[k] = self.u*self.D_aksen[k]
        b = decoding(self.S, self.K, self.D_aksen, self.a, self.u, self.v1)
        return b
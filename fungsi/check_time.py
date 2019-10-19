#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 01:02:05 2019

@author: rudi
"""

def check_time(h,tau,banyaknya_dc,banyaknya_customer):
    C=[0]*banyaknya_dc
    for j in range(banyaknya_dc):
        temp=[]
        for i in range(banyaknya_customer):
            if h[j][i] <= tau:
                temp.append(i)
        C[j] = temp
    return C

def summation_by_time(q, C):
    summation=[0]*len(q)
    for j in range(len(q)):
        summation[j]=0
        for i in range(len(C[j])):
            summation[j] = summation[j] + q[j][C[j][i]]        
    return sum(summation)
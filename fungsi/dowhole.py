#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 10:04:18 2019

@author: rudi
"""
i=0
condition = True
while condition:
    i = i+1
    print("iterasi ke ", i)
    if i % 5 ==0:
        print("berhenti")
        condition = False
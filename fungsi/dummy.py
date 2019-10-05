#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 10:22:22 2019

@author: rudi

add/remove dummy

"""
import numpy as np
#import copy
def add_dummy( source, depot, supply, demand, cost, amount_shipment):
    temp_depot = depot.copy()
    temp_demand = demand.copy()
    temp_cost = cost.copy()
    shipment_aksen= amount_shipment.copy()
    temp = [0]*len(source)
    for s in range(len(source)):
        if supply[s] - sum(amount_shipment[s]) > 0:
            temp[s] = supply[s] - sum(amount_shipment[s])
    if sum(temp) != 0:
        temp_depot.append("dummy")
        temp_demand.append(sum(temp))
        temp_cost = np.append(temp_cost, np.array([[0]*len(supply)]).T,1)
        shipment_aksen = np.append(shipment_aksen, np.array([temp]).T,1) 
        
    return shipment_aksen, temp_cost, temp_depot, temp_demand


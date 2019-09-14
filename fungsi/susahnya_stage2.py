#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:34:57 2019

@author: rudi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:27:29 2019

@author: rudi
"""
import numpy as np
import random
from repair import repair_alg
class create:
    def __init__(self, supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc):
        self.supplier = supplier
        self.plant = plant
        self.dc = dc
        self.customer = customer
        self.S = S
        self.K = K
        self.J = np.array(J)
        self.I = I
        self.maks_plant = maks_plant
        self.maks_dc = maks_dc
    def dc_to_customer(self):
        q = np.array([[0]*len(self.I)]*len(self.J))
        Od = [None]*len(self.J)
        temp_I = [0]*len(self.I)
        temp_customer = [0]*len(self.I)
        for j in range(len(self.J)):
            Od[j] = self.J[j]
        for i in range(len(self.I)):
            temp_I[i] = self.I[i]
            temp_customer[i] = self.customer[i]
        Cd = []
        y = np.array([[0]*len(self.I)]*len(self.J))
        z = np.array([0]*len(self.J))
        d_tot_cap = 0
        for j in range(len(self.J)):
            d_tot_cap = d_tot_cap + self.J[j]
        d_tot_dem = sum(self.I)
        if len(Od) > self.maks_dc or d_tot_cap < d_tot_dem:
             Od = repair_alg(Od, Cd, self.maks_dc, len(Od), d_tot_cap, d_tot_dem)   
        for je in range(len(Od)):
            temporary = np.where(self.J==Od[je])
            print('temporary',temporary)
#            print(len(temporary[0]))
#            print('ini apa ya', np.where(Od==Od[je])[0])
            if len(temporary[0]) > 1 and len(np.where(Od==Od[je])[0]) > 1:
                for i in range(len(temporary[0])):
                    z[temporary[0][i]]=1
            elif len(temporary[0]) > 1 and len(np.where(Od==Od[je])[0]) == 1:
                rand = random.randint(0, len(temporary[0])-1)
                z[temporary[0][rand]]=1
            else:
                z[temporary] = 1
#        print(self.J)
        print('nilai', z)
#        print(Od)
        
        
        temp_j = np.array([0]*len(self.J))
        temp_d = np.array([0]*len(self.I))
        for j in range(len(self.J)):
            temp_j[j] = self.J[j]
        for i in range(len(self.I)):
            temp_d[i] = self.I[i]
        for x in range(len(self.I)):
#            print("####iterasi   ", x, "########")
            r = random.randint(0, len(temp_j)-1)
            condition= True
            while  condition:
                if z[r] == 1 :
                    y[r][x] = 1
                temp_j[r] = temp_j[r] - self.I[x]*y[r][x]
                temp_d[x] = temp_d[x] - self.I[x]*y[r][x]
#                print('r  ',  r,' dan y[r][x] = ', y[r][x])
#                print('temp_j[r] =  ', temp_j[r])
#                print('temp_d[x] =   ', temp_d[x])
#                print('total j ', sum(np.multiply(temp_j, z)))
#                print('total permintaan ', sum(temp_d))
                if sum(np.multiply(temp_j, z)) < sum(temp_d) or temp_j[r] < 0 or temp_d[r] < 0 or z[r] == 0:
                    temp_d[x] = temp_d[x] + self.I[x]*y[r][x]
                    temp_j[r] = temp_j[r] + self.I[x]*y[r][x]
                    y[r][x] = 0
                    r = random.randint(0, len(temp_j)-1) 
#                    condition = True
#                elif sum(np.multiply(temp_j, z)) > sum(temp_d) and y[r][x] == 0 :
#                    condition = True
                else:
                    break             
#        print('nilai y', y)
#        print('J ', self.J)
#        print('Od  ', Od)
#        print('d ', self.I)
#        print(type(temp_j))
#        print(type(temp_d))
        for j in range(len(self.J)):
            for i in range(len(self.I)):
                q[j][i] = self.I[i]*y[j][i]
        print("nilai q sebelum ada dummy = ", q)        
        temp = [0]*len(self.J)
        for j in range(len(self.J)):
            if self.J[j] - sum(q[j])!=0 and z[j] != 0:
                temp[j] = self.J[j] - sum(q[j])
        if sum(temp) != 0:
            temp_customer.append("dummy")
            temp_I.append(sum(temp))
            q = np.append(q, np.array([temp]).T,1)
#        print('custpmer setelah ada dummy = ', temp_customer)
#        print('permintaan customer setelah ada dummy = ', temp_I)
        return z, q, y, temp_customer, temp_I

        
supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

# supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc

stage_satu = create(supplier, plant, dc, customer, sups, D, W, d, 2, 3)
#print(stage_satu.supplier_to_plant())
print(stage_satu.dc_to_customer()) 
#print("5555")
#print(stage_satu.dc_to_customer()) # karena tidak bisa sesuai dengan apa yang terjadi sesungguhnya


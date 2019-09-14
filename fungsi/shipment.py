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
        ### sebagai himpunan ###
        self.supplier = supplier
        self.plant = plant
        self.dc = dc
        self.customer = customer
#        self.Od = Od
#        self.Cd = Cd
#        self.Op = Op
#        self.Cp = Cp
        ### sebagai value
        self.S = S
        self.K = K
        self.J = J
        self.I = I
        self.maks_plant = maks_plant
        self.maks_dc = maks_dc
    def supplier_to_plant(self):
        b = np.array([[1000]*len(self.K)]*len(self.S))
        p = [1]*len(self.K)
        Op = [None]*len(self.K)
        temp_K = [None]*len(self.K)
        temp_plant = [None]*len(self.K)
        Cp = []
        for k in range(len(self.K)):
            Op[k] = self.plant[k]
            temp_K[k] = self.K[k]
            temp_plant[k] = self.plant[k]
        while len(Op) > self.maks_plant:
            rd = random.randint(0, len(Op)-1)
            Cp.append(Op[rd])
            p[self.plant.index(Op[rd])] = 0
            Op.remove(Op[rd])            
        for s in range(len(self.S)):
            while sum(b[s]) > self.S[s]:
                for k in range(len(self.K)):
                    if p[k] != 0:
                        b[s][k] = random.randint(0, self.S[s])
                    else:
                        b[s][k] = 0
        temp = [0]*len(self.S)
        for s in range(len(self.S)):
            if self.S[s] - sum(b[s])!=0:
                temp[s] = self.S[s] - sum(b[s])
        if sum(temp) != 0:
            temp_plant.append("dummy")
            temp_K.append(sum(temp))
            b = np.append(b, np.array([temp]).T,1)
        print("nilai b     ", b)
        return b, p, temp_plant, temp_K
    def dc_to_customer(self):
        q = np.array([[0]*len(self.I)]*len(self.J))
        Od = [None]*len(self.J)
        j_temp = [None]*len(self.J)
        temp_I = [0]*len(self.I)
        temp_customer = [0]*len(self.I)
        for j in range(len(self.J)):
            Od[j] = self.J[j]
            j_temp[j] = self.J[j]
        j_temp = np.array(j_temp)
        Od =np.array(Od)
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
        print("jtemps      ", j_temp)
        print("ku print juga od," ,  Od)
        for je in range(len(Od)):
            temporary = np.where(j_temp==Od[je])
#            print("kalo ini temporarrynya      ", temporary)
#            print('temporary',temporary)
#            print(len(temporary[0]))
#            print(type(Od))
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
#        print('nilai', z)
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
         
        print("nilai z    ", z)
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
            if self.J[j]*z[j] - sum(q[j]) > 0:
                temp[j] = self.J[j] - sum(q[j])
        if sum(temp) != 0:
            temp_customer.append("dummy")
            temp_I.append(sum(temp))
            q = np.append(q, np.array([temp]).T,1)
#        print('custpmer setelah ada dummy = ', temp_customer)
#        print('permintaan customer setelah ada dummy = ', temp_I)
        print("nilai q setelah ada dummy = ", q) 
        
        return q, z, y, temp_customer, temp_I

    def plant_to_dc(self):
        u = 1
        f = np.array([[1000]*len(self.J)]*len(self.K))
        stg_1 = create(self.supplier, self.plant, self.dc, self.customer,self.S,self.K,self.J,self.I, self.maks_plant, self.maks_dc).supplier_to_plant()
        b = stg_1[0]
        p = stg_1[1]
        stg_3 = create(self.supplier, self.plant, self.dc, self.customer,self.S,self.K,self.J,self.I, self.maks_plant, self.maks_dc).dc_to_customer()
        q = stg_3[0]
        z = stg_3[1]
        
        
#        for j in range(len(self.J)):
#            while sum(f[:,j]) != sum(q[j]):
#                for k in range(len(self.K)):
#                    if p[k] == 0 or z[j] == 0:
#                        f[k][j] = 0
#                    else:
#                        f[k][j] = random.randint(0, self.K[k])
##        
#                    '''
#                    jadi mungkin begini
#                    '''
#        for j in range(len(self.J)):
#            for k in range(len(self.K)):
#                while u*sum(f[k]) > self.K[k]*p[k]:
#                    if p[k] != 0 and z[j] != 0:
#                        f[k][j] = random.randint(0, self.K[k])
#                   while u*sum(f[k]) > self.K[k]*p[k] or u*sum(f[k]) > sum(b[:,k]):
#                        if p[k] == 0 or z[j] == 0:
#                            f[k][j] = 0
#                        else:
#                            f[k][j] = random.randint(0, self.K[k])
        
        for k in range(len(self.K)):
            x = 0
            for s in range(len(self.S)):
                x = x + b[s][k]
            while u*sum(f[k]) > x or u*sum(f[k]) > self.K[k]*p[k]:
#                print("k adalah", k)
                for j in range(len(self.J)):
                    while sum(f[:, j] != sum(q[j])): #bisa jadi salah
                        for k in range(len(self.K)):
                            for x in range(len(self.J)):
                                if p[k] == 0 or z[x] == 0:
                                    f[k][x] = 0
                                else:
                                    f[k][x] = random.randint(0, self.K[k])
        print("nilai p    ", p)                    
        print("nilai f sebelum dummy ", f)
        temp = [0]*len(self.K)
        for k in range(len(self.K)):
#            print('iterasi ke-',k)
#            print(sum(f[k]))
#            print(self.K[k])
            if u*self.K[k]*p[k] - sum(f[k]) > 0: #tadinya saya tidak pakai u dan di dperoleh hasil dummynya negatif
                temp[k] = self.K[k] - sum(f[k])
        if sum(temp) != 0:
            self.dc.append("dummy")
            self.J.append(sum(temp))
            f = np.append(f, np.array([temp]).T,1)
        print("nilai f  setelah dummy   ", f)
#        return f, self.dc, self.J, q, b


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
print(stage_satu.plant_to_dc()) 
#print("5555")
#print(stage_satu.dc_to_customer()) # karena tidak bisa sesuai dengan apa yang terjadi sesungguhnya


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
bisa jadi yang utama
"""
import numpy as np
import random
from repair import repair_alg
from cari_f import create_f
from cari_f import create_b
#from create_y_alg import define_y
class create:
    def __init__(self, supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc):
        self.supplier = supplier
        self.plant = plant
        self.dc = dc
        self.customer = customer
        self.S = S
        self.K = K
        self.J = J
        self.I = I
        self.maks_plant = maks_plant
        self.maks_dc = maks_dc
    def dc_to_customer(self):
        q = np.array([[0]*len(self.I)]*len(self.J))
        q_aksen = np.array([[0]*len(self.I)]*len(self.J))
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
#        print('total permintaan  ', d_tot_dem)
#        print('total persediaan   ', d_tot_cap)
        if len(Od) > self.maks_dc or d_tot_cap < d_tot_dem:
             Od = repair_alg(Od, Cd, self.maks_dc, len(Od), d_tot_cap, d_tot_dem)   
#        print("jtemps      ", j_temp)
#        print("ku print juga od," ,  Od)
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
#        print('y   ', y)
        
#        y = define_y(self.I, self.dc, self.J, y, z)
##        while y:
##            y = define_y(self.I, self.dc, self.J, y, z)
        temp_j = np.array([0]*len(self.J))
        temp_d = np.array([0]*len(self.I))
        for j in range(len(self.J)):
            temp_j[j] = self.J[j]
        for i in range(len(self.I)):
            temp_d[i] = self.I[i]
        
        x=0
#        for x in range(len(self.I)):
        while x < len(self.I):
#            print("####iterasi   ", x, "########")
            r = random.randint(0, len(temp_j)-1)
            
            condition= True
            l=0
#            temp_random = []
            temp_random_j = []
            while  condition:
                l=l+1
#                print('l  ',l)
#                print('nilai r ', r)
                if z[r] == 1 :
                    y[r][x] = 1
                temp_j[r] = temp_j[r] - self.I[x]*y[r][x]
                temp_d[x] = temp_d[x] - self.I[x]*y[r][x]
#                print('r  ',  r,' dan y[r][x] = ', y[r][x])
#                print('temp_j[r] =  ', temp_j[r])
#                print('temp_d[x] =   ', temp_d[x])
#                print('z[r]  ',z[r] )
#                print('total j ', sum(np.multiply(temp_j, z)))
#                print('total permintaan ', sum(temp_d))
                if l == 50 : break
                if sum(np.multiply(temp_j, z)) < sum(temp_d) or temp_j[r] < 0 or temp_d[r] < 0 or z[r] == 0:
                    temp_d[x] = temp_d[x] + self.I[x]*y[r][x]
                    temp_j[r] = temp_j[r] + self.I[x]*y[r][x]
                    y[r][x] = 0
                    ###dibuat handler untuk r yg memungkinkan mendapat nilai yang sama terus###
#                    temp_random.append(r)
                    temp_random_j.append(self.dc[r])
                    r = random.randint(0, len(temp_j)-1) 
#                    print(temp_random_j)
#                    print(self.dc)
#                    print(len(set(self.dc)-set(temp_random_j)))
#                    print(np.where(np.array(temp_random)==r)[0])
#                    s=0
                    if len(temp_random_j) != 0 and len(set(temp_random_j)-set(self.dc)) == 0:
                        for j in range(len(self.J)):
                            temp_j[j] = self.J[j]
                        for i in range(len(self.I)):
                            temp_d[i] = self.I[i]
                        y = np.array([[0]*len(self.I)]*len(self.J))
                        x = -1
                        break

                else:
                    break        
            x = x+1
        for j in range(len(self.J)):
            for i in range(len(self.I)):
                q[j][i] = self.I[i]*y[j][i]
                q_aksen[j][i] = self.I[i]*y[j][i]
#        print("nilai q sebelum ada dummy = ", q)        
        temp = [0]*len(self.J)
        for j in range(len(self.J)):
            if self.J[j]*z[j] - sum(q[j]) > 0:
                temp[j] = self.J[j] - sum(q[j])
        if sum(temp) != 0:
            temp_customer.append("dummy")
            temp_I.append(sum(temp))
            q_aksen = np.append(q_aksen, np.array([temp]).T,1)
#        print('custpmer setelah ada dummy = ', temp_customer)
#        print('permintaan customer setelah ada dummy = ', temp_I)
#        print("nilai q setelah ada dummy = ", q) 
        
        return q, z, y, temp_customer, temp_I,q_aksen
    def plant_to_dc(self):
#        u = 1
        temp_J = [0]*len(self.J)
        temp_dc = [0]*len(self.J)
#        for j in range(len(self.J)):
            
        f = np.array([[0]*len(self.J)]*len(self.K))
        stg_3 = create(self.supplier, self.plant, self.dc, self.customer,self.S,self.K,self.J,self.I, self.maks_plant, self.maks_dc).dc_to_customer()
        q = stg_3[0]
        z = stg_3[1]
        tot_dem = 0
        ka = [0]*len(self.K)
#        Pd = [0]*len(self.K)
        for j in range(len(self.J)):
            tot_dem = tot_dem + sum(q[j])
            temp_J[j] = self.J[j]*z[j]
            temp_dc[j] = self.dc[j]
#            Pd[k] = self.v2[k]
        tot_cap = 0
        p = [1]*len(self.K)
        for k in range(len(self.K)):
            tot_cap = tot_cap+ self.K[k]*p[k]
        Op = [None]*len(self.K)
        Cp = []
        for k in range(len(self.K)):
            Op[k] = self.plant[k]
            ka[k] = self.K[k]
#        print(Op)
#        print(self.plant)
        Cp = list(set(self.plant)-set(Op))
#        Np = len(Op)
#        print('Cp  ', Cp)
        P = 2
        temp_k = np.array(self.plant)
        temp_op = np.array(Op)
        temp_cp = np.array(Cp)
#        print('tot_dem   ', tot_dem)
        if tot_dem < 450:    
            i=0
            while len(Op) > P or tot_cap < tot_dem: 
                i= i+1
#                print('i ', i )
                index_op =[]
                for m in range(len(temp_op)):
                    index_op.append(int(np.where(temp_k == temp_op[m])[0]))
                dok =[]
                for x in range(len(index_op)):
                    dok.append(ka[index_op[x]])
                    
                
                index_cp = []
                for m in range(len(temp_cp)):
                    index_cp.append(int(np.where(temp_k == temp_cp[m])[0]))
    #            index_cp = np.where(temp_k == temp_cp)150
                dck=[]
                for y in range(len(index_cp)):
                    dck.append(ka[index_cp[y]])   
                    
                dop = len(dok)
                dp = P
                d_tot_cap = tot_cap
                d_tot_dem = tot_dem
                dok = repair_alg(dok, dck, dp, dop, d_tot_cap, d_tot_dem)
                Op  = []
                p = [1]*len(self.K)
                tot_cap = sum(dok)
#                print('dok  ', dok)
                temp_De = np.array(self.K)
                
                ## memasukkan Plant dengan kapasitas yang sama
                if len(dok) > 1 and max(dok)==min(dok):
                    indexofop = np.where(temp_De == dok[0])[0]
                    for x in range(len(indexofop)):
                        Op.append(self.plant[indexofop[x]])     
                    ##
                else:
                    for k in range(len(dok)):
                        if len(np.where(temp_De == dok[k])[0]) >1:
                            indexofop = np.where(temp_De == dok[k])[0]
                            rand = random.randint(0, len(indexofop)-1)
                            Op.append(self.plant[indexofop[rand]])
#                            print("masuk sini ")
                        else:
                            Op.append(self.plant[self.K.index(dok[k])])     
#                            print("mlebu sini ")
#                print('Op ',Op)
                
                Cp =list(set(self.plant)-set(Op))            
#                print('Cp ',Cp)
                if i == 10:#cuma dipakai ketika iterasinya tidak berhenti (handler)
                    break   
            for s in range(len(Cp)):
                dck.append(self.K[self.plant.index(Cp[s])])
            for j in range(len(Cp)):
                p[self.plant.index(Cp[j])] = 0

        f = create_f(self.plant, self.dc, self.K, self.J, p, z, q) 
        f_aksen=np.array([[None]*len(self.J)]*len(self.K))
        for k in range(len(self.K)):
            for j in range(len(self.J)):
                f_aksen[k][j]=f[k][j]
        temp = [0]*len(self.K)
        for k in range(len(self.K)):
            if self.K[k]*p[k] - sum(f[k]) > 0:
                temp[k] = self.K[k] - sum(f[k])
        if sum(temp) != 0:
            temp_dc.append("dummy")
            temp_J.append(sum(temp))
            f_aksen = np.append(f_aksen, np.array([temp]).T,1)
        print('nilai z  ', z)
#        print('dc setelah ada dummy = ', temp_dc)
#        print('permintaan dc setelah ada dummy = ', temp_J)
#        print("nilai f setelah ada dummy = ", f_aksen) 
        return f, q, p, f_aksen
    
    
    def supplier_to_plant(self):
        temp_plant = [None]*len(self.K)
        temp_K =[None]*len(self.K)
        for k in range(len(self.K)):
            temp_plant[k] = self.plant[k]
            temp_K[k] = self.K[k]
        b = np.array([[0]*len(self.K)]*len(self.S))
        stg_2 = create(self.supplier, self.plant, self.dc, self.customer,self.S,self.K,self.J,self.I, self.maks_plant, self.maks_dc).plant_to_dc()
        f = stg_2[0]
        q = stg_2[1]
        p = stg_2[2]        
        b= create_b(self.supplier, self.plant, self.S, self.K, p, f)
        b_aksen=np.array([[None]*len(self.K)]*len(self.S))
        for s in range(len(self.S)):
            for k in range(len(self.K)):
                b_aksen[s][k]=b[s][k]
        temp = [0]*len(self.S)
        for s in range(len(self.S)):
            if self.S[s] - sum(b[s]) > 0:
                temp[s] = self.S[s] - sum(b[s])
        if sum(temp) != 0:
            temp_plant.append("dummy")
            temp_K.append(sum(temp))
            b_aksen = np.append(b_aksen, np.array([temp]).T,1)
#        print('nilai p  ', p)
#        print('plant setelah ada dummy = ', temp_plant)
#        print('permintaan plant setelah ada dummy = ', temp_K)
#        print("nilai b setelah ada dummy = ", b_aksen) 
        return b, f, q, b_aksen
    
    
supplier = ["s1","s2","s3"]
plant = ["p1","p2","p3"]
dc = ["dc1","dc2","dc3","dc4"]
customer =["cust1","cust2", "cust3","cust4"]

sups =[250,200,250]
D = [200,150,200] 
W = [150, 100, 200, 100]
d = [50, 100, 50, 100]

# supplier, plant, dc, customer,S,K,J,I, maks_plant, maks_dc

stage_satu = create(supplier, plant, dc, customer, sups, D, W, d, 2, 2).supplier_to_plant()
#print(stage_satu.supplier_to_plant())
#print('print b', stage_satu[0])
#print('print f', stage_satu[1])
#print('print q', stage_satu[2]) 
#print("5555")
print(stage_satu) # karena tidak bisa sesuai dengan apa yang terjadi sesungguhnya


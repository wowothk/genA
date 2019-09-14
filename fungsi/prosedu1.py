# encoding stage 3 (integer encoding)
import numpy as np

def int_encode(dc, customer, g):
    # dengan g merupakan kapasitas yang dikirimkan dari dc_j ke kustomer i
    temp_dc = [0]*len(dc)
    temp_customer = [0]*len(customer)
    v= [0]*len(customer)

    for j in range(len(dc)):
        temp_dc[j] = dc[j]
    
    for i in range(len(customer)):
        temp_customer[i] = customer[i]

    for j in range(len(dc)):
        for k in range(len(customer)):
            if g[j][k] != 0:
                v[k] = j+1 
    
    return v

# dc = [150,100,200, 100, 50]
# customer = [50,100, 50, 100, 50]

# g=np.array([[50, 100, 0, 0, 0], [0,0,0,0,0],[0,0,50,100,50],[0,0,0,0,0],[0,0,0,0,0]])

# v = int_encode(dc, customer, g)
# print(v)

### decoding stage 3 ####
# input
# J : set of DC
# I : set of customer
# W_j : capacity of dc_j
# d_i : demand for product of customer i
# v_3 : chromosom 
# output
# O_D : set of opened DCs
# C_D : set of closed DCs
# q_ij : the amount of product shipped from DC_j to customer i
# W_j' : total demand for product on DC_j

def int_decode(J, I, W, d, v):
    z=[0]*len(J)
    y=np.array([[0]*len(I)]*len(J))
    O_D=[]
    C_D=J
    q = np.array([[0]*len(I)]*len(J))
    W_aksen = [0]*len(J)
    tot_cap=0
    # tot_dem=0
    temp_W = [0]*len(J)
    for j in range(len(J)):
        temp_W[j] = W[j]

    for i in range(len(I)):
        z[v[i]] = 1
        y[i][v[i]] = 1
        O_D.append(v[i])
        C_D.remove(v[i])
    
    for j in range(len(J)):
        tot_cap = tot_cap + W[j]*z[j]
    
    tot_dem = sum(d)
    sum_od = sum(z)

    if sum_od <= len(J) and tot_cap >= tot_dem:
        for i in range(len(I)):
            q[i][v[i]]=d[i] # kalau ada salah mungkin dapa diperhatikan di sini
            temp_W[v[i]] = temp_W[v[i]]-q[i][v[i]]
            W_aksen[v[i]] = W_aksen[v[i]] + q[i][v[i]]       
            d[i]=0
        for j in range(len(J)):
            if temp_W[j] < 0:
                for i in range(len(I)):
                    y[i][j] = 0
                    for j in range(len(J)):
                        if temp_W[j]-q[i][j]>=0:
                            y[i][j] = 1
                            break
        v = int_encode(temp_W,d,q)
        int_decode(temp_W, I, d, v)
        return temp_W, W_aksen, q
    else:
        DOK = O_D
        DCK = C_D
        DOP = len(O_D)
        DP = len(J)
        d_tot_cap = tot_cap
        d_tot_dem = tot_dem
        from repair import repar_alg
        repair_alg(DOK, DCK, DP, DOP, d_tot_cap, d_tot_dem)
        # setelah direpair dia hanya menghasilkan DOK lalu apa hubungannya dengan pembentukan kromosom?
        
    return    

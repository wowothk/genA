## prosedur 4 decoding stage 2 ##
# input
# K : set of plants, J : set of DCs, P : maximum number of plants
# W′ j : total customer demand for product on DC j, ∀j ∈ J,
# a_jk : shipping cost of one unit of product from plant k to DC j,∀k∈K,∀j∈J,
# v 2 ((k+j)) : chromosome, ∀k ∈ K, ∀j ∈ J,

#output
# f kj : the amount of product shipped from plant k to DC j
# D′_k : total customer demand for product on plant k, ∀k ∈ K,
# p(k) : priority of plant k for product, ∀k ∈ K,
# NP : number of opened plants, o P : set of opened plants,
# tot_cap : total capacity of opened plants
# tot_dem : total demand of DCs
import numpy as np 
def decode_pb_2(K, W_aksen, a, v):
    # dimana a merupakan shipping cost 

    q = np.array([[0]*len(K)]*len(J))
    D =[0]*len(K)
    tot_dem = 0
    ####
    f_kj
    NP
    tot_cap
    P
    ###
    for k in range(len(K)):
        for j in range(len(J)):
            tot_dem = tot_dem + q[k][j]
    
    p=[0]*len(K)
    p_d= [0]*len(K)
    for k in range(len(K)+len(J)):
        if k < len(K):
            p[k] = v[k]
            p_d[k] = p[k]

    temp=0
    index=0
    while tot_cap < tot_dem and NP<P:
        for k in range(len(K)):
            if temp == 0:
                temp = p_d[k]
                index = k
            elif p_d[k]>temp:
                temp = p_d[k]
                index = k
        hp_k=index
        p[hp_k] = 1
        tot_cap = tot_cap + D[hp_k]
        NP = NP+1
        p_d[hp_k] = 0
        O_p = O_p + index
    
    for k in range(len(K)+len(J)):
        v[k] = 0 if p[k] == 0

    if O_p <= P and tot_cap >= tot_dem:
        from prosedur1 import decoding
        decoding()
    else:
        DOK = O_p
        DCK = list(set(K)-set(O_p))
        DOP = NP
        DP = P 
        d_tot_cap, d_tot_dem = tot_cap, tot_dem
        from repair import repair_alg
        repair_alg()
        ## balik ke langkah3


        


        
    

    
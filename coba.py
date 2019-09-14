# Encoding algorithm for parity based encoding

import numpy as np 
# C as cost
# C = np.array([[11,19,17,18],[16,14,18,15],[15,16,19,13]])
# depot = [300, 350, 300, 350]
# sources = [550,300,450]
# g = np.array([[300,0,250,0],[0,300,0,0],[0,50,50,350]])

# v as chromosom


def encoding(C,sources, depot, g):
    v = [None]*(len(depot)+len(sources))
    p = len(depot)+len(sources)
    i=0
    index=[0,0]
    while depot[index[1]] != 0 or sources[index[0]] != 0:
        temp_c = 0 
        for k in range(len(sources)):
            for j in range(len(depot)):
                if g[k][j] != 0 and (depot[j] == g[k][j] or sources[k]==g[k][j]):
                    if temp_c == 0:
                        temp_c=C[k][j]
                        index[0] = k
                        index[1] = j
                    elif C[k][j] < temp_c:
                        temp_c = C[k][j]
                        index[0] = k
                        index[1] = j
        depot[index[1]] = depot[index[1]]-g[index[0]][index[1]]
        sources[index[0]] = sources[index[0]]-g[index[0]][index[1]]                
        if depot[index[1]] == 0 :
            v[len(sources)+index[1]] = p 
            p = p-1
            g[index[0]][index[1]] = 0
        if  sources[index[0]] == 0 :
            v[index[0]] = p 
            p = p-1
            g[index[0]][index[1]] = 0
    return v

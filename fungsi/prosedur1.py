## decoding prosedur 1 ###

import numpy as np
def decoding(sources, depot, b, a, c ,v):

    temp_a = [None]*len(a)
    temp_b= [None]*len(b)
    for k in range(len(sources)):
        temp_a[k] = a[k]

    for j in range(len(depot)):
        temp_b[j]=temp_b[j]

    g = np.array([[0]*len(depot)]*len(sources))
    k=0
    j=0
    index=[0,0]
    i=0
    while sum(v) !=0:
        temp_c =0
        for x in range(len(v)):
            if v[x] == max(v) and x < len(sources):
                k = x
                for jl in range(len(depot)):
                    if v[len(sources)+jl] != 0:
                        if temp_c == 0:
                            temp_c = c[k][jl]
                            index[0]=k
                            index[1]=jl
                        elif c[k][j] < temp_c:
                            temp_c = c[k][jl]
                            index[0]=k
                            index[1]=jl
                j = index[1]
            elif v[x] == max(v) and x >= len(sources):
                j = x - len(sources)
                for kl in range(len(sources)):
                    if v[kl] != 0 :
                        if temp_c == 0:
                            temp_c = c[kl][j]
                            index[0]=kl
                            index[1]=j
                        elif c[kl][j]<temp_c:
                            temp_c = c[kl][j]
                            index[0]=kl
                            index[1]=j
                k=index[0]
        g[k][j] = min(temp_sources[k], temp_depot[j])
        temp_a[k] = temp_a[k]-g[k][j]
        temp_b[j] = temp_b[j]-g[k][j]
        if temp_sources[k] == 0:
            v[k] = 0
        if temp_depot[j] == 0:
            v[len(sources)+j]= 0
    return g

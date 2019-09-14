import numpy as np
def decoding(C,sources, depot,v):
    g = np.array([[0]*len(depot)]*len(sources))
    sources = 
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
                            temp_c = C[k][jl]
                            index[0]=k
                            index[1]=jl
                        elif C[k][j] < temp_c:
                            temp_c = C[k][jl]
                            index[0]=k
                            index[1]=jl
                j = index[1]
            elif v[x] == max(v) and x >= len(sources):
                j = x - len(sources)
                for kl in range(len(sources)):
                    if v[kl] != 0 :
                        if temp_c == 0:
                            temp_c = C[kl][j]
                            index[0]=kl
                            index[1]=j
                        elif C[kl][j]<temp_c:
                            temp_c = C[kl][j]
                            index[0]=kl
                            index[1]=j
                k=index[0]
        g[k][j] = min(sources[k], depot[j])
        sources[k] = sources[k]-g[k][j]
        depot[j] = depot[j]-g[k][j]
        if sources[k] == 0:
            v[k] = 0
        if depot[j] == 0:
            v[len(sources)+j]= 0
    return g
    
import numpy as np
def decoding(C,sources, depot,v):
    temp_sources = [None]*len(sources)
    temp_depot= [None]*len(depot)
    for k in range(len(sources)):
        temp_sources[k] = sources[k]

    for j in range(len(depot)):
        temp_depot[j]=depot[j]

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
        g[k][j] = min(temp_sources[k], temp_depot[j])
        temp_sources[k] = temp_sources[k]-g[k][j]
        temp_depot[j] = temp_depot[j]-g[k][j]
        if temp_sources[k] == 0:
            v[k] = 0
        if temp_depot[j] == 0:
            v[len(sources)+j]= 0
    return g

def encoding(C,sources, depot, g):
    temp_sources = [None]*len(sources)
    temp_depot= [None]*len(depot)
    for k in range(len(sources)):
        temp_sources[k] = sources[k]

    for j in range(len(depot)):
        temp_depot[j]=depot[j]

    v = [None]*(len(depot)+len(sources))
    p = len(depot)+len(sources)
    i=0
    index=[0,0]
    while temp_depot[index[1]] != 0 or temp_sources[index[0]] != 0:
        i=i+1
        print(i)
        temp_c = 0 
        for k in range(len(sources)):
            for j in range(len(depot)):
                if g[k][j] != 0 and (temp_depot[j] == g[k][j] or temp_sources[k]==g[k][j]):
                    if temp_c == 0:
                        temp_c=C[k][j]
                        index[0] = k
                        index[1] = j
                    elif C[k][j] < temp_c:
                        temp_c = C[k][j]
                        index[0] = k
                        index[1] = j
        temp_depot[index[1]] = temp_depot[index[1]]-g[index[0]][index[1]]
        temp_sources[index[0]] = temp_sources[index[0]]-g[index[0]][index[1]]                
        if temp_depot[index[1]] == 0 :
            v[len(sources)+index[1]] = p 
            p = p-1
            g[index[0]][index[1]] = 0
        if  temp_sources[index[0]] == 0 :
            v[index[0]] = p 
            p = p-1
            g[index[0]][index[1]] = 0
    return v
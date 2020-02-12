### repair algorithm ###
### input ###
# DOK ; Set of opened sources;
# DCK : Set of closed sources;
# DP : maximum number of sources
# DOP : number of opened sources
# d_tot_cap : total capacity of opened sources
# d_tot_dem : total requirement of depots

### output ###
# DOK : set of opened sources
from random import randint

def repair_alg(DOK, DCK, DP, DOP, d_tot_cap, d_tot_dem):
    temp_dok = [0]*len(DOK)
    temp_dck = [0]*len(DCK)

    for x in range(len(DOK)):
        temp_dok[x]=DOK[x]
    
    for y in range(len(DCK)):
        temp_dck[y]=DCK[y]
    i=0        
    while DOP > DP or d_tot_cap < d_tot_dem:
        i=i+1
#        if i == 50: 
#            break
#        print(i)
#        print(d_tot_cap)
#        print(d_tot_dem)
#        print(DOP)
#        print(DP)
        if DOP > DP and d_tot_cap >= d_tot_dem:
            while DOP > DP:
                if len(temp_dok) != 0:
                    index = randint(0,len(temp_dok)-1)
                    temp = temp_dok[index]
                    del temp_dok[index]
                    temp_dck.append(temp)
                    DOP = len(temp_dok)
            d_tot_cap = sum(temp_dok)
        elif (DOP<DP or DOP >= DP) and d_tot_cap< d_tot_dem:
            while d_tot_cap < d_tot_dem:
                if len(temp_dck) != 0:
                    index = randint(0, len(temp_dck)-1)
                    temp = temp_dck[index]
                    del temp_dck[index]
                    temp_dok.append(temp)
                d_tot_cap = sum(temp_dok)
            DOP = len(temp_dok)
    return temp_dok
    




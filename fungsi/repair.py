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
#    print('dcl  ', len(temp_dck))
    while DOP != DP or d_tot_cap < d_tot_dem:    
        if DOP > DP and d_tot_cap >= d_tot_dem:
            while DOP > DP:
                if len(temp_dok) != 0:
                    index = randint(0,len(temp_dok)-1)
                    temp = temp_dok[index]
                    del temp_dok[index]
                    temp_dck.append(temp)
                    DOP = len(temp_dok)
            d_tot_cap = sum(temp_dok)
            
    #        return temp_dok
    #            else:
    #                index = randint(0,len(temp_dok))
    #                temp = temp_dok[index]
    #                del temp_dok[index]
    #                temp_dck.append(temp)
    #        return temp_dok        
            
        if (DOP<DP or DOP >= DP) and d_tot_cap< d_tot_dem:
            while d_tot_cap < d_tot_dem:
                if len(temp_dck) != 0:
    #                index = randint(0, len(temp_dck))
    #            else:
                    index = randint(0, len(temp_dck)-1)
    #                print('temp_dck    ', temp_dck)
    #                print('index   ' ,index)
                    temp = temp_dck[index]
                    del temp_dck[index]
                    temp_dok.append(temp)
                d_tot_cap = sum(temp_dok)
            DOP = len(temp_dok)
    return temp_dok
    

#sumber = ['s1', 's2', 's3']
#tujuan = ['p1', 'p2', 'p3', 'dummy']
#tujuan_val = [200, 0, 200, 150]
#sumber_val = [250, 200, 250]
#
#d_cap = sum(sumber_val)
#d_dem = sum(tujuan_val)
#
#DOP = 




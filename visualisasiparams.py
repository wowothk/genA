import pandas as pd 
import math
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_excel("perbandinganparameter2000.xlsx")

# f, axes = plt.subplots(3, 3, sharex=True)
f, axes = plt.subplots(3, 3)
listpc = sorted(list(set(data.pc.dropna())))

# f1
# for pc in range(len(listpc)):    
#     dt = data[data.pc==listpc[pc]]
#     dvis = dict()
#     for i in set(dt.pm):
#         df = dt[dt.pm==i]
#         dvis[str(i)] = (df.f1.mean(),df.f2.mean())

#     dvis = pd.DataFrame({
#         "$p_{m}$": list(dvis.keys()),
#         "$f_{1}$": [i[0] for i in dvis.values()],
#         "$f_{2}$": [i[1] for i in dvis.values()]
#     })
#     if pc%3 == 0:        
#         a = sns.lineplot(x="$p_{m}$",y="$f_{1}$", data=dvis, ax=axes[int(pc/3)][0])
#         axes[int(pc/3)][0].legend(["$p_{c}$="+str(listpc[pc])])
#     elif pc%3 == 1:
#         a = sns.lineplot(x="$p_{m}$",y="$f_{1}$", data=dvis, ax=axes[math.floor(pc/3)][1])
#         axes[math.floor(pc/3)][1].legend(["$p_{c}$="+str(listpc[pc])])
#     else:
#         a = sns.lineplot(x="$p_{m}$",y="$f_{1}$", data=dvis, ax=axes[math.floor(pc/3)][2])
#         axes[math.floor(pc/3)][2].legend(["$p_{c}$="+str(listpc[pc])])

# f.suptitle("Grafik Rata-Rata $f_{1}$ Pada Setiap Iterasi $p_{m}$ Untuk Suatu $p_{c}$")
# plt.show()

# f2

# for pc in range(len(listpc)):    
#     dt = data[data.pc==listpc[pc]]
#     dvis = dict()
#     for i in set(dt.pm):
#         df = dt[dt.pm==i]
#         dvis[str(i)] = (df.f1.mean(),df.f2.mean())

#     dvis = pd.DataFrame({
#         "$p_{m}$": list(dvis.keys()),
#         "$f_{1}$": [i[0] for i in dvis.values()],
#         "$f_{2}$": [i[1] for i in dvis.values()]
#     })
#     if pc%3 == 0:        
#         a = sns.lineplot(x="$p_{m}$",y="$f_{2}$", data=dvis, ax=axes[int(pc/3)][0])
#         axes[int(pc/3)][0].legend(["$p_{c}$="+str(listpc[pc])])
#         # a.set_title("Grafik Rata-Rata $f_{1}$ pada tiap iterasi $p_{m}$ untuk $p_{c}$="+str(listpc[pc]))
#     elif pc%3 == 1:
#         a = sns.lineplot(x="$p_{m}$",y="$f_{2}$", data=dvis, ax=axes[math.floor(pc/3)][1])
#         axes[math.floor(pc/3)][1].legend(["$p_{c}$="+str(listpc[pc])])
#         # a.set_title("Grafik Rata-Rata $f_{1}$ pada tiap iterasi $p_{m}$ untuk $p_{c}$="+str(listpc[pc]))
#     else:
#         a = sns.lineplot(x="$p_{m}$",y="$f_{2}$", data=dvis, ax=axes[math.floor(pc/3)][2])
#         axes[math.floor(pc/3)][2].legend(["$p_{c}$="+str(listpc[pc])])
#         # a.set_title("Grafik Rata-Rata $f_{1}$ pada tiap iterasi $p_{m}$ untuk $p_{c}$="+str(listpc[pc]))
# f.suptitle("Grafik Rata-Rata $f_{2}$ Pada Setiap Iterasi $p_{m}$ Untuk Suatu $p_{c}$")
# plt.show()

# pareto
for pc in range(len(listpc)):    
    dt = data[data.pc==listpc[pc]]
    dvis = dict()
    for i in set(dt.pm):
        df = dt[dt.pm==i]
        dvis[str(i)] = (df.f1.mean(),df.f2.mean())

    dvis = pd.DataFrame({
        "$p_{m}$": list(dvis.keys()),
        "$f_{1}$": [i[0] for i in dvis.values()],
        "$f_{2}$": [i[1] for i in dvis.values()]
    })
    if pc%3 == 0:        
        a = sns.scatterplot(x="$f_{1}$",y="$f_{2}$",hue="$p_{m}$", data=dvis, legend=False, palette="bright", ax=axes[int(pc/3)][0])
        # axes[int(pc/3)][0].legend(["$p_{c}$="+str(listpc[pc])])
    elif pc%3 == 1:
        a = sns.scatterplot(x="$f_{1}$",y="$f_{2}$",hue="$p_{m}$", data=dvis, legend=False, palette="bright",ax=axes[math.floor(pc/3)][1])
        axes[math.floor(pc/3)][1].set_ylabel('')
        # axes[math.floor(pc/3)][1].legend(["$p_{c}$="+str(listpc[pc])])
    else:
        a = sns.scatterplot(x="$f_{1}$",y="$f_{2}$",hue="$p_{m}$", data=dvis, legend=False, palette="bright",ax=axes[math.floor(pc/3)][2])
        axes[math.floor(pc/3)][2].set_ylabel('')
        # axes[math.floor(pc/3)][2].legend(["$p_{c}$="+str(listpc[pc])])

col = sns.color_palette("bright").as_hex()
# to create legend but not bullet
# import matplotlib.patches as mpathces
# handles = list()
# for i in range(len(sorted(list(set(dt.pm))))):
#     handles.append(mpathces.Patch(color=col[i]))

# to create bullet
patches = [plt.plot([],[], marker="o", ms=5, ls="",                  mec=None, color=col[i])[0]  for i in range(len(sorted(list(set(dt.pm))))) 
]

f.legend(title='$p_{m}$', handles=patches, labels=sorted(list(set(dt.pm))), loc="center right")

f.suptitle("Grafik Rata-Rata Solusi Optimal Pareto")
plt.show()
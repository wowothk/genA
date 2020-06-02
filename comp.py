import pandas as pd 

data = pd.read_excel("populasimore.xlsx")

avg_f1 = dict()
avg_f2 = dict()
generations = [(i+1)*100 for i in range(20)]


i = 1
for j in generations:
    k = int(i+j/10)
    avg_f1[str(j)] = data.iloc[i:k,1][data.generasi==j].mean()
    avg_f2[str(j)] = data.iloc[i:k,2][data.generasi==j].mean()   
    i = k

df = pd.DataFrame({"generasi":list(avg_f1.keys()),"avg_f1":list(avg_f1.values()), "avg_f2":list(avg_f2.values())})
print(df.tail())
import matplotlib.pyplot as plt
import seaborn as sns

f, axes = plt.subplots(1, 2) 

a = sns.lineplot(x="generasi",y="avg_f1", sort=False, data=df, ax=axes[0])

a.set_xticklabels(df.generasi, rotation=45, horizontalalignment='right')
a.set_title("Grafik Rata-Rata Nilai $f_{1}$ pada tiap iterasi")

b = sns.lineplot(x="generasi",y="avg_f2", sort=False, data=df, ax=axes[1])
b.set_xticklabels(df.generasi, rotation=45, horizontalalignment='right')
b.set_title("Grafik Rata-Rata Nilai $f_{2}$ pada tiap iterasi")

plt.show()

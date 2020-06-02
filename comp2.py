import pandas as pd 

data = pd.read_excel("populasi.xlsx")

generations = [(i+1)*100 for i in range(20)]

f1=dict()
f2=dict()

i = 1
for j in generations:
    k = int(i+j/100)
    f1[str(j)] = int(data.iloc[i:k,1][data.generasi==j])
    f2[str(j)] = float(data.iloc[i:k,2][data.generasi==j])
    i = k

df = pd.DataFrame({"generasi":list(f1.keys()),"$f_{1}$":list(f1.values()), "$f_{2}$":list(f2.values())})
import matplotlib.pyplot as plt
import seaborn as sns

f, axes = plt.subplots(1, 2) 

a = sns.lineplot(x="generasi",y="$f_{1}$", sort=False, data=df, ax=axes[0])

a.set_xticklabels(df.generasi, rotation=45, horizontalalignment='right')
a.set_title("Grafik Nilai $f_{1}$ pada tiap iterasi")

b = sns.lineplot(x="generasi",y="$f_{2}$", sort=False, data=df, ax=axes[1])
b.set_xticklabels(df.generasi, rotation=45, horizontalalignment='right')
b.set_title("Grafik Nilai $f_{2}$ pada tiap iterasi")

plt.show()
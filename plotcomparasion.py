import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np

sns.set(style="white")

df = pd.read_excel("compare.xlsx")

datapm1 = df[df["pm"]==0.1]
datapm2 = df[df["pm"]==0.2]

# Plot miles per gallon against horsepower with other semantics
# sns.relplot(x="f1", y="f2", hue="pc", size="pm",
#             sizes=(40, 400), alpha=.5, palette="muted",
#             height=6, data=df)

# fig, axes = plt.subplots(len(df.pm),2)

# cmap = sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)
# sns.relplot(x="f1", y="f2", size="pc", hue="pc",
#             sizes=(40, 400), alpha=0.5, palette="bright", legend="full",
#             data=datapm1)

# for i in range(1):
#     j = int(np.round(i/2))
#     if i%2==0:
#         sns.scatterplot(x="f1", y="f2", size="pc", hue="pc",
#                                     sizes=(40, 400), alpha=0.5, palette="bright", 
#                                     legend="full", data=df[df.pm == df.pm[i]], ax=axes[j,0])
#     else:
#         sns.scatterplot(x="f1", y="f2", size="pc", hue="pc",
#                                     sizes=(40, 400), alpha=0.5, palette="bright", 
#                                     legend="full", data=df[df.pm == df.pm[i]], ax=axes[j,1])




# fig, axes = plt.subplots(1,1)

sns.scatterplot(x="f1", y="f2", size="pc", hue="pc",
                                    sizes=(40, 400), alpha=0.5, palette="bright", 
                                    legend="full", data=df[df.pm == 0.9])
# axes[0].set_title("p${_m}$=0.9")

# sns.scatterplot(x="f1", y="f2", size="pc", hue="pc",
#                                     sizes=(40, 400), alpha=0.5, palette="bright", 
#                                     legend="full", data=df[df.pm == 0.8], ax=axes[1])
# axes[1].set_title("p$_{m}$=0.8")

plt.title("p${_m}$=0.9")
# plt.tight_layout()
plt.show()


# g = sns.FacetGrid(df, hue="pc", col="pm", height=4,
#                   hue_kws={"marker": ["s", "D"]})
# g.map(plt.scatter, "f1", "f2", s=40, edgecolor="w")
# g.add_legend();

# plt.show()



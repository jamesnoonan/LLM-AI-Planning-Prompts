import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.lines as mlines

# Parameters
size = (8, 5)
padding = 0.1
top_spacing = 0.02 # for title
bottom_spacing = 0.06 # for legend

labels = ["NL Basic", "NL Intermediate", "NL Detailed", "PDDL"]
markers = ['o', '^', 's', 'P']

cmap = plt.get_cmap('Blues')

#
# Generate graph
# 

# Create dataframe from csv data
df = pd.read_csv("data.csv")

# Find the sets of properties of the data
obstacle_count = df['obstacle_count']
unique_sizes = df['size'].unique()
representation_types = df.copy().drop(columns=["size", "obstacle_density", "obstacle_count"]).columns

# Create figure and suplots, with two columns
figure = plt.figure(figsize=size)

for i, representation_type in enumerate(representation_types):
    plt.scatter(
        obstacle_count,
        df[representation_type] * 100,
        label=labels[i],
        c=df["size"],
        cmap=cmap,
        vmin=3,
        vmax=11,
        marker=markers[i])

figure.suptitle("Effect of No. of Obstacles on Performance", y=0.95, fontsize=16)
plt.xlabel("Number of Obstacles")
plt.ylabel("LLM Success Rate (% valid)")

leg = figure.legend(handles=[
    mlines.Line2D([], [], color="cornflowerblue", marker=markers[0], ls='', label=labels[0]),
    mlines.Line2D([], [], color="cornflowerblue", marker=markers[1], ls='', label=labels[1]),
    mlines.Line2D([], [], color="cornflowerblue", marker=markers[2], ls='', label=labels[2]),
    mlines.Line2D([], [], color="cornflowerblue", marker=markers[3], ls='', label=labels[3]),
], loc='lower center', ncols=4)


plt.subplots_adjust(left=padding, right=1-(padding/2), bottom=padding + bottom_spacing, top=1-padding-top_spacing)
plt.savefig('scatter_graph.png')
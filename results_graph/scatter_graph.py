import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
# Parameters
size = (10, 7)
padding = 0.08
top_spacing = 0.03 # for title
bottom_spacing = 0.05 # for legend

# Spacing between graphs
w_padding_internal = 0.06
h_padding_internal = 0.35

bar_width = 0.2

labels = ["NL Basic", "NL Intermediate", "NL Detailed", "PDDL"]
colors = ["xkcd:blue", "xkcd:green", "xkcd:gold", "xkcd:red"]


# color_map_name = 'tab20b' # The colors of the series of data
# cmap = plt.get_cmap(color_map_name)
# colors = cmap(np.arange(len(representation_types)))

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
    plt.scatter(obstacle_count, df[representation_type], label=labels[i], color=colors[i], marker='o')

figure.suptitle('ChatGPT 3.5 Navigation Planning Performance', y=0.97, fontsize=16)
figure.legend(labels=labels, loc='lower center', ncols=4)

plt.subplots_adjust(left=padding, right=1-(padding/2), bottom=padding + bottom_spacing, top=1-padding-top_spacing, wspace=w_padding_internal, hspace=h_padding_internal)
plt.savefig('scatter_graph.png')
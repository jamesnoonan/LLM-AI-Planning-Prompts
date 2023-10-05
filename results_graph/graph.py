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

color_map_name = 'tab10' # The colors of the series of data

#
# Generate graph
# 

# Create dataframe from csv data
df = pd.read_csv("data.csv")

# Find the sets of properties of the data
unique_densities = df['obstacle_density'].unique()
unique_sizes = df['size'].unique()
representation_types = df.copy().drop(columns=["size", "obstacle_density"]).columns

# Summarise graph to be created
print(f"\n\nGenerating graph with {len(unique_densities)} obstacle densities, {len(unique_sizes)} grid sizes with these representation types:\n{representation_types}\n\n")

x = np.arange(np.min(unique_sizes), np.max(unique_sizes) + 1)
graph_count = len(unique_densities)

cmap = plt.get_cmap(color_map_name)
# colors = cmap(np.linspace(0, 1, len(representation_types)))
colors = cmap(np.arange(len(representation_types)))

# Create figure and suplots, with two columns
figure, ax = plt.subplots(int(graph_count / 2), 2, sharey=True, figsize=size)

# Iterate over the different obstacle densities, and create a graph for each
for i in range(graph_count):
    obstacle_density = unique_densities[i]

    row = int(i / 2)
    col = i % 2
    subplot = ax[row][col]

    multiplier = 0
    for index, representation_type in enumerate(representation_types):
        offset = bar_width * multiplier # Find the offset of this series

        # Get the data for this series
        plot_data = df[df['obstacle_density'] == obstacle_density]
        # Plot the bar chart, with the calculated offset
        subplot.bar(plot_data['size'] + offset,
                    plot_data[representation_type] * 100,
                    width=bar_width,
                    label=representation_type,
                    color=colors[index])

        multiplier += 1 # Increment mutliplier for next offset

    subplot.set_title(f'{int(obstacle_density * 100)}% Obstacle Density', fontsize=11)
   
    # if ((row+1) == int(graph_count/2)):
    subplot.set_xlabel('Grid Size')
    if (col == 0):
        subplot.set_ylabel('Accuracy (% correct)')

    subplot.set_xticks(x + 2*bar_width, x)

    subplot.set_ylim(0, 100)

figure.suptitle('ChatGPT 3.5 Navigation Planning Performance', y=0.97, fontsize=16)
figure.legend(labels=representation_types, loc='lower center', ncols=4)

plt.subplots_adjust(left=padding, right=1-padding, bottom=padding + bottom_spacing, top=1-padding-top_spacing, wspace=w_padding_internal, hspace=h_padding_internal)
plt.savefig('graphs.png')
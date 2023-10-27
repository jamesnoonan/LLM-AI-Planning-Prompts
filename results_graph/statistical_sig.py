import pandas as pd
from scipy.stats import spearmanr
import pingouin as pg

df = pd.read_csv("data.csv")

# Sample data (replace this with your actual data)
grid_size = []
obstacle_count = []
accuracy = []

representation_types = df.copy().drop(columns=["size", "obstacle_density", "obstacle_count"]).columns
# for representation_type in representation_types:
for representation_type in ["pddl"]:
    grid_size.extend(df['size'])
    obstacle_count.extend(df['obstacle_count'])
    accuracy.extend(df[representation_type])

# Calculate the Spearman rank correlation
def correleation(x):
    spearman_corr, p_value = spearmanr(x, accuracy)

    print(f"Spearman Rank Correlation: {spearman_corr}")
    print(f"P-value: {p_value}")

    if p_value < 0.05:
        print("There is a statistically significant relationship.")
    else:
        print("There is no statistically significant relationship.")

def partial_correleation(x, covar):
    df = pd.DataFrame({
        'grid_size': grid_size,
        'accuracy': accuracy,
        'obstacle_count': obstacle_count,
    })

    partial_corr = pg.partial_corr(data=df, x=x, y='accuracy', method='spearman', covar=covar)

    print(partial_corr)
    if partial_corr['p-val'].iloc[0] < 0.05:
        print("There is a statistically significant relationship.")
    else:
        print("There is no statistically significant relationship.")

# print("--- GRID SIZE ---")
# correleation(grid_size)

# print("\n--- OBSTACLE COUNT ---")
# correleation(obstacle_count)

print("--- GRID SIZE ---")
partial_correleation('grid_size', 'obstacle_count')

print("\n--- OBSTACLE COUNT ---")
partial_correleation('obstacle_count', 'grid_size')

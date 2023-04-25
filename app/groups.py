import pandas as pd
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import numpy as np

# Read data from CSV
df = pd.read_csv('app/groups.csv')

# Create graph
G = nx.Graph()

# Add nodes
for index, row in df.iterrows():
    G.add_node(row['name'])

# Add edges with attributes
for index, row in df.iterrows():
    name = row['name']
    work_well = row['work_well'].strip('"').split()
    not_work_well = row['not_work_well'].strip('"').split()
    
    for w in work_well:
        G.add_edge(name, w, type='work_well')
    for nw in not_work_well:
        G.add_edge(name, nw, type='not_work_well')

# Group formation function
def form_groups(G, group_size=4):
    def form_group_recursively(node, group, remaining_nodes):
        if len(group) == group_size:
            return group
        
        for neighbor in G.neighbors(node):
            if neighbor in remaining_nodes:
                new_group = group + [neighbor]
                new_remaining_nodes = remaining_nodes - {neighbor}
                result = form_group_recursively(neighbor, new_group, new_remaining_nodes)
                if result:
                    return result
        return None

    groups = []
    nodes = set(G.nodes())

    while nodes:
        node = nodes.pop()
        group = form_group_recursively(node, [node], nodes)
        if group:
            groups.append(group)
            nodes = nodes - set(group)

    return groups

groups = form_groups(G)

# Print groups
for i, group in enumerate(groups, start=1):
    print(f"Group {i}: {', '.join(group)}")

# Visualization
pos = nx.spring_layout(G, seed=42)
node_colors = []

color_map = plt.cm.get_cmap('viridis', len(groups) + 1)

for node in G.nodes:
    found = False
    for i, group in enumerate(groups):
        if node in group:
            node_colors.append(color_map(i))
            found = True
            break
    if not found:
        node_colors.append(color_map(len(groups)))  # Assign a color to nodes not in any group

edge_colors = ['green' if G.edges[e]['type'] == 'work_well' else 'red' for e in G.edges]
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_size=8, node_size=1000, edge_color=edge_colors)
plt.show()

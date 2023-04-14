import networkx as nx
import matplotlib.pyplot as plt
import csv

# Load the data from the CSV file
with open('data/Sociogram survey(1-10).csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Create a new graph
G = nx.Graph()

# Add the nodes to the graph
for row in rows:
    G.add_node(row['name'])

# Add the edges to the graph
for row in rows:
    name = row['name']
    for work_well in row['work_well'].split(','):
        work_well = work_well.strip()
        if work_well != '':
            if row['not_work_well'] != '':
                not_work_well = row['not_work_well'].split(',')
                not_work_well = [s.strip() for s in not_work_well]
                if name in not_work_well and work_well in not_work_well:
                    G.add_edge(name, work_well, color='red')
                elif name in not_work_well:
                    G.add_edge(name, work_well, color='orange')
                else:
                    other_row = [r for r in rows if r['name'] == work_well][0]
                    other_work_well = [s.strip() for s in other_row['work_well'].split(',')]
                    if name in other_work_well:
                        G.add_edge(name, work_well, color='green')
                    else:
                        G.add_edge(name, work_well, color='blue')
            else:
                G.add_edge(name, work_well, color='blue')

# Draw the graph with different colors for edges representing different relationships
pos = nx.spring_layout(G)

# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
nx.draw_networkx_labels(G, pos, font_size=12, font_family='Arial')

# Draw edges with different colors
for edge_color, edges_list in [('green', []), ('blue', []), ('orange', []), ('red', [])]:
    for u, v in G.edges():
        if G[u][v]['color'] == edge_color:
            edges_list.append((u, v))
    nx.draw_networkx_edges(G, pos, edgelist=edges_list, edge_color=edge_color)

plt.axis('off')
plt.show()



# If both nodes work well together, the 'color' attribute is set to 'green'
# If only one node works well with the other, the 'color' attribute is set to 'blue'
# If one node does not work well with the other, the 'color' attribute is set to 'orange'
# If both nodes do not work well with each other, the 'color' attribute is set to 'red'
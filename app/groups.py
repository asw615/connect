import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import community

# read CSV file into pandas DataFrame
df = pd.read_csv('/Users/sorenmeiner/Desktop/connected/app/static/data/survey.csv')

# Get unique classes
classes = df['class'].unique()

for class_name in classes:
    class_df = df[df['class'] == class_name]
    
    # get list of all unique names in the class
    names = class_df['name'].unique()
    n = len(names)

    # initialize n x n matrix with zeros
    matrix = np.zeros((n, n))

    def get_set_of_names(name_list):
        if pd.isna(name_list):
            return set()
        return set(name_list.split(', '))

    # iterate over rows and fill in matrix
    for i, name_i in enumerate(names):
        for j, name_j in enumerate(names[i+1:], start=i+1):
            work_well_i = get_set_of_names(class_df.loc[class_df['name'] == name_i, 'work_well'].values[0])
            not_work_well_i = get_set_of_names(class_df.loc[class_df['name'] == name_i, 'not_work_well'].values[0])
            work_more_with_i = get_set_of_names(class_df.loc[class_df['name'] == name_i, 'work_more_with'].values[0])

            work_well_j = get_set_of_names(class_df.loc[class_df['name'] == name_j, 'work_well'].values[0])
            not_work_well_j = get_set_of_names(class_df.loc[class_df['name'] == name_j, 'not_work_well'].values[0])
            work_more_with_j = get_set_of_names(class_df.loc[class_df['name'] == name_j, 'work_more_with'].values[0])

            if name_i in not_work_well_j or name_j in not_work_well_i:
                matrix[i, j] = -1
                matrix[j, i] = -1
            elif name_i in work_well_j and name_j in work_well_i:  # if mutual work well
                matrix[i, j] = 2
                matrix[j, i] = 2
            elif name_i in work_well_j or name_j in work_well_i:  # if one-sided work well
                matrix[i, j] = 1
                matrix[j, i] = 1
            elif name_i in work_more_with_j or name_j in work_more_with_i:  # if one wants to work more with the other
                matrix[i, j] = 2
                matrix[j, i] = 2

        # create graph from matrix
    G = nx.from_numpy_array(matrix)

    # Calculate the total weight of edges
    m = G.size(weight='weight')

    # If total weight is zero, create a single community with all individuals
    if m == 0:
        communities = [frozenset(range(n))]
    else:
        # perform modularity optimization
        communities = community.greedy_modularity_communities(G, weight='weight')


    # sort communities by size
    communities = sorted(communities, key=len, reverse=True)

    # create groups of specified size
    group_size = 4
    groups = []
    current_group = []
    for community in communities:
        for name in community:
            current_group.append(name)
            if len(current_group) == group_size:
                groups.append(current_group)
                current_group = []

        if current_group:
            while len(current_group) < group_size and groups:
                current_group.append(groups[-1].pop())
                if not groups[-1]:
                    groups.pop()
            if current_group:
                groups.append(current_group)
# print groups
names = names.tolist()
print(f"\nClass: {class_name}")
for i, group in enumerate(groups):
    group_names = [names[index] for index in group]
    print(f"Group {i+1}: {', '.join(sorted(group_names))}")

# handle any leftover individuals
if current_group:
    print(f"Leftover: {', '.join(sorted([names[index] for index in current_group]))}")


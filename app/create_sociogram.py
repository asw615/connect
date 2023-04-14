import igraph as ig
import csv

def create_sociogram(class_name):
    with open('app/static/data/survey.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row['class'] == class_name]

    G = ig.Graph()

    for row in rows:
        G.add_vertex(row['name'])

    node_names = G.vs["name"]

    for row in rows:
        name = row['name']
        for work_well in row['work_well'].split(','):
            work_well = work_well.strip()
            if work_well != '' and work_well in node_names:
                e = G.get_eid(name, work_well, error=False)
                if e == -1:
                    G.add_edge(name, work_well, color=None)

    # Define edge colors
    for row in rows:
        name = row['name']
        for work_well in row['work_well'].split(','):
            work_well = work_well.strip()
            if work_well != '' and work_well in node_names:
                e = G.get_eid(name, work_well, error=False)
                if e != -1:
                    edge = G.es[e]
                    if edge["color"] is None:
                        edge["color"] = "blue"
                    elif edge["color"] == "blue":
                        edge["color"] = "green"

        for not_work_well in row['not_work_well'].split(','):
            not_work_well = not_work_well.strip()
            if not_work_well != '' and not_work_well in node_names:
                e = G.get_eid(name, not_work_well, error=False)
                if e != -1:
                    edge = G.es[e]
                    if edge["color"] is None:
                        edge["color"] = "orange"
                    elif edge["color"] == "orange":
                        edge["color"] = "red"
                else:
                    other_person_row = next(r for r in rows if r["name"] == not_work_well)
                    if name in other_person_row["not_work_well"]:
                        G.add_edge(name, not_work_well, color="red")

    # Define edge widths
    edge_widths = [0] * len(G.es)
    for e, edge in enumerate(G.es):
        if edge["color"] == "green":
            edge_widths[e] = 4
        elif edge["color"] == "blue":
            edge_widths[e] = 3
        elif edge["color"] == "orange":
            edge_widths[e] = 2
        elif edge["color"] == "red":
            edge_widths[e] = 1

    # Visualize the graph
    visual_style = {}
    visual_style["vertex_size"] = 70
    visual_style["vertex_color"] = "lightblue"
    visual_style["vertex_label"] = G.vs["name"]
    visual_style["edge_color"] = G.es["color"]
    visual_style["layout"] = G.layout_fruchterman_reingold()
    visual_style["bbox"] = (800, 800)
    visual_style["margin"] = 50
    visual_style["edge_width"] = edge_widths

    plot = ig.plot(G, **visual_style)
    plot.save("sociogram.png")


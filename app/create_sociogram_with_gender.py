import igraph as ig
import csv
import cairocffi as cairo


def create_sociogram(class_name):
    with open('app/static/data/survey.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row['class'] == class_name]

    G = ig.Graph()

    for row in rows:
        G.add_vertex(row['name'], gender=row['gender'])

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
                        edge["color"] = "steelblue2"
                    elif edge["color"] == "steelblue2":
                        edge["color"] = "mediumseagreen"

        for not_work_well in row['not_work_well'].split(','):
            not_work_well = not_work_well.strip()
            if not_work_well != '' and not_work_well in node_names:
                e = G.get_eid(name, not_work_well, error=False)
                if e != -1:
                    edge = G.es[e]
                    if edge["color"] is None:
                        edge["color"] = "darkorange"
                    elif edge["color"] == "darkorange":
                        edge["color"] = "slateblue1"
                else:
                    other_person_row = next(r for r in rows if r["name"] == not_work_well)
                    if name in other_person_row["not_work_well"]:
                        G.add_edge(name, not_work_well, color="slateblue1")

    # Define edge widths
    edge_widths = [0] * len(G.es)
    for e, edge in enumerate(G.es):
        if edge["color"] == "mediumseagreen":
            edge_widths[e] = 3
        elif edge["color"] == "steelblue2":
            edge_widths[e] = 3
        elif edge["color"] == "darkorange":
            edge_widths[e] = 3
        elif edge["color"] == "slateblue1":
            edge_widths[e] = 3

    # Define vertex shapes and labels
    shapes = {
        'Male': 'square',
        'Female': 'circle',
        'Other': 'triangle'
    }
    vertex_shapes = [shapes[gender] for gender in G.vs['gender']]
    vertex_labels = [None] * len(G.vs)
    for i, name in enumerate(G.vs["name"]):
        vertex_labels[i] = name

    # Visualize the graph
    visual_style = {}
    visual_style["vertex_size"] = 70
    visual_style["vertex_shape"] = vertex_shapes
    visual_style["vertex_label"] = vertex_labels
    visual_style["vertex_label_color"] = "white"
    visual_style["vertex_label_size"] = 15
    visual_style["vertex_label_dist"] = 1
    visual_style["vertex_label_angle"] = -45
    visual_style["edge_color"] = G.es["color"]
    visual_style["layout"] = G.layout_fruchterman_reingold()
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 50
    visual_style["edge_width"] = edge_widths

    # Load images
    male_image = cairo.ImageSurface.create_from_png("app/static/images/male.png")
    female_image = cairo.ImageSurface.create_from_png("app/static/images/female.png")
    other_image = cairo.ImageSurface.create_from_png("app/static/images/other.png")
    
    def draw_vertex_images(context, vertices, drawer):
        for vertex in vertices:
            x, y = vertex['x'], vertex['y']
            image = images[G.vs[vertex.index]['gender']]
            w, h = image.get_width(), image.get_height()
            context.save()
            context.translate(x - w / 2, y - h / 2)
            context.set_source_surface(image)
            context.paint()
            context.restore()
    images = {
        'Male': male_image,
        'Female': female_image,
        'Other': other_image
    }
    vertex_images = [images[gender] for gender in G.vs['gender']]
    visual_style["vertex_shape"] = vertex_images

    plot = ig.plot(G, **visual_style, mark_groups=None, drawer_factory=ig.drawing.CairoCffiDrawer)
    plot.redraw(draw_vertex_images)
    plot.save("sociogram.png")


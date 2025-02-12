'''Generated with chatgpt'''

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as mpatches

# Create a new directed graph with cleaner layout
G_clean = nx.DiGraph()

# Define refined nodes
nodes_clean = {
    "Local Raster Dataset": {"type": "data_source"},
    "Web API": {"type": "data_source"},
    "Climate Data Connector": {"type": "connector"},
    "Climate Data Outputs": {"type": "output"},  # Combined outputs
    "Chap-core (Python Package)": {"type": "consumer"},
    "Prediction App": {"type": "consumer"},
    "Climate App": {"type": "consumer"},
    "DHIS2": {"type": "consumer"},  # Now the same as other consumers
    "Other Applications": {"type": "consumer"},
    "Endusers": {"type": "end_user"}  # Renamed and generalized
}

# Add refined edges
edges_clean = [
    ("Local Raster Dataset", "Climate Data Connector"),
    ("Web API", "Climate Data Connector"),
    ("Climate Data Connector", "Climate Data Outputs"),
    ("Climate Data Outputs", "Chap-core (Python Package)"),
    ("Climate Data Outputs", "Prediction App"),
    ("Climate Data Outputs", "Climate App"),
    ("Climate Data Outputs", "DHIS2"),
    ("Climate Data Outputs", "Other Applications"),
    ("Chap-core (Python Package)", "Endusers"),
    ("Prediction App", "Endusers"),
    ("Climate App", "Endusers"),
    ("DHIS2", "Endusers"),
    ("Other Applications", "Endusers")
]

# Add nodes and edges to the graph
for node, attr in nodes_clean.items():
    G_clean.add_node(node, **attr)

G_clean.add_edges_from(edges_clean)

# Define new node colors for clarity
color_map_clean = {
    "data_source": "lightblue",
    "connector": "orange",
    "output": "lightgreen",
    "consumer": "lightcoral",  # Unified consumers (Chap-core, Apps, DHIS2)
    "end_user": "yellow"
}

node_colors_clean = [color_map_clean[nodes_clean[node]["type"]] for node in G_clean.nodes()]

# Define a structured layout with fixed positions
pos_clean = {
    "Local Raster Dataset": (-2, 1),
    "Web API": (-2, -1),
    "Climate Data Connector": (0, 0),
    "Climate Data Outputs": (2, 0),
    "Chap-core (Python Package)": (4, 1.5),
    "Prediction App": (4, 0.5),
    "Climate App": (4, -0.5),
    "DHIS2": (4, -1.5),
    "Other Applications": (4, -2.5),
    "Endusers": (6, 0)
}

# Draw refined graph with straight edges and rounded rectangles
plt.figure(figsize=(10, 6))
ax = plt.gca()
nx.draw_networkx_nodes(G_clean, pos_clean, node_color=node_colors_clean, node_size=2500, node_shape="s", edgecolors="black")
nx.draw_networkx_labels(G_clean, pos_clean, font_size=9, font_weight="bold")
nx.draw_networkx_edges(G_clean, pos_clean, edge_color="black", width=1.5, arrows=True, connectionstyle="arc3,rad=0.0")

# Add legend
patches = [mpatches.Patch(color=color, label=label) for label, color in color_map_clean.items()]
plt.legend(handles=patches, loc="upper right", title="Legend")

# Title and display
plt.title("Refined System Architecture: Climate Data Connector", fontsize=12)
plt.axis("off")
plt.show()

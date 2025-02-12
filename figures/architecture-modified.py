import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib.patches as mpatches
import pathlib

output_folder = pathlib.Path(__file__).parent

# Utilities
def draw_manhattan_edges(ax, pos, edges, direction="horizontal", color="black", lw=1.5):
    """ Draw edges with 90-degree turns """
    for edge in edges:
        x1, y1 = pos[edge[0]]  # Start node position
        x2, y2 = pos[edge[1]]  # End node position

        # Compute midpoint (turning point)
        if direction == "horizontal":
            mid_x = x2  # Move horizontally first
            mid_y = y1  # Then move vertically
        else:  # "vertical"
            mid_x = x1  # Move vertically first
            mid_y = y2  # Then move horizontally

        # Create path with two segments
        path = mpatches.Path([(x1, y1), (mid_x, mid_y), (x2, y2)], [mpatches.Path.MOVETO, mpatches.Path.LINETO, mpatches.Path.LINETO])
        patch = mpatches.PathPatch(path, edgecolor=color, linewidth=lw, facecolor="none", linestyle="solid")
        ax.add_patch(patch)

def draw_midpoint_arrows(ax, pos, edges, color="black", arrow_size=15):
    """
    Draw arrows at the midpoint of each edge in the correct direction.
    """
    for edge in edges:
        x1, y1 = pos[edge[0]]  # Start node
        x2, y2 = pos[edge[1]]  # End node

        # Compute midpoint
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2

        # Compute direction vector (small step in direction of the edge)
        dx, dy = (x2 - x1) * 0.2, (y2 - y1) * 0.2  # Scale down so arrow doesn't extend too far

        # Add arrow annotation
        ax.annotate(
            "",
            xy=(mid_x + dx, mid_y + dy),  # Shift arrow tip slightly forward in edge direction
            xytext=(mid_x - dx, mid_y - dy),  # Base of arrow slightly backward
            arrowprops=dict(arrowstyle="->", color=color, lw=1.5, mutation_scale=arrow_size)
        )

# Create a new directed graph with cleaner layout
G_clean = nx.DiGraph()

# Define refined nodes
nodes_clean = {
    "Local Raster Dataset": {"type": "data_source"},
    "Web API": {"type": "data_source"},
    "Data Processing": {"type": "processing"},
    "Grid Data": {"type": "output"},
    "Orgunit Data": {"type": "output"},
    "Tile Server": {"type": "output"},
    "Connector API": {"type": "api"},  # Combined Connector API
    "Chap-core": {"type": "consumer"},
    "Prediction App": {"type": "consumer"},
    "Climate App": {"type": "consumer"},
    "DHIS2": {"type": "consumer"},  # Now the same as other consumers
    "Other Applications": {"type": "consumer"},
    "Endusers": {"type": "end_user"}  # Renamed and generalized
}
label_override = {
    "Data Processing": "Custom\nData\nLogic",
    "Grid Data": "Grid\nData?",
    "Orgunit Data": "Orgunit\nData",
    "Tile Server": "Tile\nServer?",
    "Connector API": "API",
    "Local Raster Dataset": "Local\nGridded\nDataset",
    "Other Applications": "Other\nApps",
    "Climate App": "Climate\nApp",
    "Prediction App": "Prediction\nApp",
}
label_dict = {k:label_override.get(k, k) for k in nodes_clean}

# Add straight line edges
edges_clean = [
    ("Local Raster Dataset", "Data Processing"),
    ("Web API", "Data Processing"),
    ("Data Processing", "Grid Data"),
    ("Data Processing", "Orgunit Data"),
    ("Data Processing", "Tile Server"),
    ("Grid Data", "Connector API"),
    ("Orgunit Data", "Connector API"),
    ("Tile Server", "Connector API"),
    ("Connector API", "Chap-core"),
    ("Connector API", "Climate App"),
    ("Connector API", "Other Applications"),
    ("Chap-core", "Prediction App"),
    ("Chap-core", "Endusers"),
    ("Prediction App", "Endusers"),
    ("Climate App", "Endusers"),
    ("Climate App", "DHIS2"),
    ("DHIS2", "Endusers"),
    ("Other Applications", "Endusers")
]

# Define subset of edges that need Manhattan routing
manhattan_edges = [
    ("Chap-core", "Endusers"),
    ("Other Applications", "Endusers"),
]

# Add nodes and edges to the graph
for node, attr in nodes_clean.items():
    G_clean.add_node(node, **attr)

G_clean.add_edges_from(edges_clean)

# Define new node colors for clarity
color_map_clean = {
    "data_source": "lightblue",
    "processing": "moccasin",
    "api": "orange",
    "output": "orange",
    "consumer": "lightcoral",  # Unified consumers (Chap-core, Apps, DHIS2)
    "end_user": "lightgreen"
}

node_colors_clean = [color_map_clean[nodes_clean[node]["type"]] for node in G_clean.nodes()]

# Base position for the data Connector API
pos_clean = {
    "Local Raster Dataset": (-2, 1),
    "Web API": (-2, -1),
    "Data Processing": (2-2.4, 0),
    "Orgunit Data": (2-1.2, 0),
    "Grid Data": (2-1.2, 1),
    "Tile Server": (2-1.2, -1),
    "Connector API": (2, 0),
    "Endusers": (6, 0)  # Keep Endusers far right
}

# List of consumer nodes
consumer_nodes = [
    "Chap-core",
    "Prediction App",
    "Climate App",
    "DHIS2",
    "Other Applications"
]

# Arrange consumers in a half-circle around (2, 0)
radius = 2  # Distance from Climate Data Connector API
angles = np.linspace(-np.pi / 2, np.pi / 2, len(consumer_nodes))  # Semi-circle from bottom to top

for node, angle in zip(consumer_nodes, angles):
    pos_clean[node] = (2 + radius * np.cos(angle), radius * np.sin(angle))

# Draw graph with straight line edges and rounded rectangles
plt.figure(figsize=(10, 6))
ax = plt.gca()
nx.draw_networkx_nodes(G_clean, pos_clean, node_color=node_colors_clean, node_size=2800, node_shape="s", edgecolors="black")
nx.draw_networkx_labels(G_clean, pos_clean, labels=label_dict, font_size=8, font_weight="bold")
nx.draw_networkx_edges(G_clean, pos_clean, edgelist=[e for e in edges_clean if e not in manhattan_edges], edge_color="black", width=1.5, arrows=False, connectionstyle="arc3")

# Draw Manhattan edges separately
draw_manhattan_edges(ax, pos_clean, manhattan_edges)

# Add midpoint arrows
#draw_midpoint_arrows(ax, pos_clean, edges_clean)

# Add legend
#patches = [mpatches.Patch(color=color, label=label) for label, color in color_map_clean.items()]
#plt.legend(handles=patches, loc="upper right", title="Legend")

# Title and display
plt.title("System Architecture: Climate Data Connector", fontsize=12, y=1.05)
plt.axis("off")
plt.savefig(output_folder / 'architecture-modified.png')

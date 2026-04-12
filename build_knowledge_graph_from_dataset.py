from sys import argv
from networkx import MultiGraph, write_graphml

DATASET = argv[1]
PATH_TRAIN = f"datasets/{DATASET}/train.txt"

graph: MultiGraph = MultiGraph()

# Load the data from the training split
with open(PATH_TRAIN, "r") as f:
    for i, line in enumerate(f):
        spl = line.strip().split("\t")
        # Skip negative examples in the training split, since we generate our own negatives
        if len(spl) >= 4 and spl[3] != "1":
            continue

        s, r, t = spl[:3]
        graph.add_edge(s, t, rel=r, key=r)

# Save the full graph data
graph_filename = f"output/{DATASET}_knowledge_graph.graphml"
write_graphml(graph, graph_filename)
print(f"Graph data saved locally as: {graph_filename}")

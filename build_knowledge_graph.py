from networkx import DiGraph, write_graphml
from tqdm import tqdm

from argparse import ArgumentParser
from glob import glob

parser = ArgumentParser()
parser.add_argument("dataset_name", type=str)
parser.add_argument("context_size", type=int, nargs="?", default=3)
args = parser.parse_args()

dataset_name, context_size = vars(args).values()
split = "train"

kg = DiGraph()

# Find all relation CSVs
file_pattern = f"output/{dataset_name}/{split}/c{context_size}/*.csv"
files = glob(file_pattern)

if not files:
    raise Exception(f"No files found for pattern: {file_pattern}")

print("Scanning files to determine total edge count...")
total_edges_to_add = 0
for file_path in files:
    with open(file_path, "r") as file:
        # Skip header
        next(file)

        for line in file:
            parts = line.strip().split(";")
            if len(parts) >= 2 and int(parts[1]) == 1:
                total_edges_to_add += 1

print(f"Found {total_edges_to_add} valid edges to process.")

with tqdm(
    total=total_edges_to_add, desc="Building Knowledge Graph", unit=" edges"
) as progress_bar:
    for file_path in files:
        with open(file_path, "r") as file:
            # Skip header
            next(file)

            for line in file:
                parts = line.strip().split(";")
                if len(parts) < 2:
                    continue

                triple_str = parts[0]
                label = int(parts[1])

                if label != 1:
                    continue

                try:
                    subject, relation, obj = triple_str.split(",")
                    kg.add_edge(subject, obj, label=relation)
                except ValueError:
                    continue
                finally:
                    progress_bar.update(1)

print(
    f"\nConstructed graph with {kg.number_of_nodes()} nodes and {kg.number_of_edges()} edges."
)

# Save the full graph data
graph_filename = f"output/{dataset_name}/{split}/knowledge_graph.graphml"
write_graphml(kg, graph_filename)
print(f"Graph data saved locally as: {graph_filename}")

print(f"\nFile processed: {', '.join(files)}")

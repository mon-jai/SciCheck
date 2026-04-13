from argparse import ArgumentParser
from sys import exit
from typing import cast, Literal, Tuple

from networkx import MultiGraph, write_graphml

parser = ArgumentParser()
parser.add_argument("source", type=str)
parser.add_argument("dataset", type=str)

args = parser.parse_args()
SOURCE, DATASET = cast(Tuple[Literal["datasets", "output"], str], vars(args).values())

if SOURCE not in ("datasets", "output"):
    print("Invalid source. Source must be either datasets or output.")
    exit(1)

DATA_DIR = f"{SOURCE}/{DATASET}"
EXT = "txt" if SOURCE == "datasets" else "csv"
CSV_FILE_PATHS = (f"{DATA_DIR}/train.{EXT}", f"{DATA_DIR}/test.{EXT}")

graph: MultiGraph = MultiGraph()
id_count: int = 0


def process_csv(csv_file_path):
    global graph, id_count
    try:
        with open(csv_file_path, "r") as file:
            for line in file:
                if SOURCE == "datasets":
                    spl = line.strip().split("\t")
                else:
                    attributes = line.split(";")
                    tuple = attributes[0].split(",")
                    label = attributes[1]
                    spl = [*tuple, label]

                # Skip negative examples in the data
                if len(spl) >= 4 and spl[3] != "1":
                    continue

                s, r, t = spl[:3]
                graph.add_edge(s, t, rel=r, key=id_count)
                id_count += 1
    except FileNotFoundError:
        print(f"{csv_file_path} was not found.")
        exit(1)


# Load the data
for csv_file_path in CSV_FILE_PATHS:
    process_csv(csv_file_path)

# Save the full graph data
graph_filename = f"output/{SOURCE}_{DATASET}_knowledge_graph.graphml"
write_graphml(graph, graph_filename)
print(f"Graph data saved locally as: {graph_filename}")

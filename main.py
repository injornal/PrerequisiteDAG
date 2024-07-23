"""Made by Kostia"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def main() -> None:
    """main function"""
    prerequisites: pd.DataFrame = pd.read_csv("prerequisites.csv")
    G = nx.DiGraph()
    groups: dict[str, set[str]] = {}

    color_list: list[str] = [
        "green",
        "red",
        "blue",
        "purple",
        "orange",
        "yellow",
        "brown",
        "gray", 
        "magenta",
    ]
    for line in prerequisites.values:
        if not line[2] in groups:
            groups[line[2]] = {line[0]}
        else:
            groups[line[2]].add(line[0])

    color_map: dict[str, str] = {}
    for course_set in groups.values():
        # retreats the last color from the color_list as the current color
        color: str = color_list.pop()
        for course in course_set:
            if not isinstance(course, str):  # if NaN or None etc.
                continue
            color_map[course] = color

    for line in prerequisites.values:
        if isinstance(line[0], str) and isinstance(line[1], str):
            G.add_edge(line[1], line[0])
        elif isinstance(line[0], str):
            G.add_node(line[0])

    for layer, nodes in enumerate(nx.topological_generations(G)):
        for node in nodes:
            G.nodes[node]["layer"] = layer

    pos = nx.multipartite_layout(G, subset_key="layer")

    # assigns each node a color
    node_colors: list[str] = [color_map[node] for node in G.nodes]

    fig, ax = plt.subplots()

    nx.draw_networkx(G, pos=pos, ax=ax, node_color=node_colors)
    ax.set_title("DAG layout in topological order")
    fig.tight_layout()
    plt.show()  # type: ignore[no-untyped-call]


if __name__ == "__main__":
    main()

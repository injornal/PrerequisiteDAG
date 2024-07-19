import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def main():
    prerequisites: pd.DataFrame = pd.read_csv("prerequisites.csv")
    G = nx.DiGraph()
    nodes: dict = {}
    for line in prerequisites.values:
        if line[1] is not None and line[0] is not None:
            G.add_edge(line[1], line[0])
    for layer, nodes in enumerate(nx.topological_generations(G)):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer value as a node attribute
        for node in nodes:
            G.nodes[node]["layer"] = layer

    # Compute the multipartite_layout using the "layer" node attribute
    pos = nx.multipartite_layout(G, subset_key="layer")

    fig, ax = plt.subplots()
    nx.draw_networkx(G, pos=pos, ax=ax)
    ax.set_title("DAG layout in topological order")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()


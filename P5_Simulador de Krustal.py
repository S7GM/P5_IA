import networkx as nx
import matplotlib.pyplot as plt

#   DIBUJAR GRAFO Y ARBOL

def dibujar_grafo(G, mst_edges, step, modo):
    plt.clf()
    pos = nx.spring_layout(G, seed=42)

    # Nodos
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color="#6aa4ff")

    # Todas las aristas en gris
    nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=2)

    # Etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    # Pesos
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Aristas del árbol en rojo
    if mst_edges:
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=mst_edges,
            width=3,
            edge_color="red",
        )

    titulo_modo = "Mínimo" if modo == "min" else "Máximo"
    plt.title(f"Árbol de {titulo_modo} Coste con Kruskal - Paso {step}")
    plt.pause(1)


#   UNION FIND

def make_set(nodos):
    parent = {}
    rank = {}
    for nodo in nodos:
        parent[nodo] = nodo
        rank[nodo] = 0
    return parent, rank


def find(parent, nodo):
    if parent[nodo] != nodo:
        parent[nodo] = find(parent, parent[nodo])
    return parent[nodo]


def union(parent, rank, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra == rb:
        return False
    if rank[ra] < rank[rb]:
        parent[ra] = rb
    elif rank[ra] > rank[rb]:
        parent[rb] = ra
    else:
        parent[rb] = ra
        rank[ra] += 1
    return True

def kruskal_paso_a_paso(G, modo="min"):
    edges = []
    for u, v, data in G.edges(data=True):
        w = data["weight"]
        edges.append((w, u, v))

    # Orden segun modo
    reverse = True if modo == "max" else False
    edges.sort(reverse=reverse)

    parent, rank = make_set(G.nodes())
    mst_edges = []
    costo_total = 0
    step = 1

    print("\nOrden de aristas segun el modo elegido:")
    for w, u, v in edges:
        print(f"{u} -- {v} con peso {w}")
    print()

    dibujar_grafo(G, mst_edges, step, modo)

    for w, u, v in edges:
        print(f"=== PASO {step} ===")
        print(f"Probando arista {u} -- {v} con peso {w}")

        if find(parent, u) != find(parent, v):
            print("No forma ciclo, se agrega al árbol")
            union(parent, rank, u, v)
            mst_edges.append((u, v))
            costo_total += w

            print("Aristas actuales en el árbol:")
            for a, b in mst_edges:
                print(f"  {a} -- {b} con peso {G[a][b]['weight']}")
            print(f"Costo acumulado: {costo_total}")
            step += 1
            dibujar_grafo(G, mst_edges, step, modo)
        else:
            print("Formaría un ciclo, se descarta esta arista")
        print()

        if len(mst_edges) == len(G.nodes()) - 1:
            break

    return mst_edges, costo_total


def main():
    # Mismo grafo que has usado en Prim
    edges = [
        ("A", "C", 2),
        ("A", "B", 4),
        ("C", "B", 1),
        ("C", "D", 8),
        ("B", "D", 5),
        ("D", "E", 2),
        ("C", "E", 10),
        ("E", "F", 3),
        ("D", "F", 6),
    ]

    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    print("Nodos del grafo:")
    print(", ".join(sorted(G.nodes())))
    modo_str = input(
        "Escribe MIN para árbol de mínimo coste o MAX para árbol de máximo coste: "
    ).strip().lower()

    if modo_str.startswith("max"):
        modo = "max"
    else:
        modo = "min"

    mst_edges, costo_total = kruskal_paso_a_paso(G, modo)

    titulo_modo = "mínimo" if modo == "min" else "máximo"
    print(f"\nResultado final para el árbol de {titulo_modo} coste con Kruskal:")
    for u, v in mst_edges:
        w = G[u][v]["weight"]
        print(f"{u} -- {v} con peso {w}")
    print(f"Costo total del árbol: {costo_total}")

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    plt.ion()
    main()
M

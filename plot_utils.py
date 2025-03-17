# plot_utils.py

import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

def get_hierarchy_pos(root, x_factor=2.0):
    """
    Distribuye los nodos de manera que la raíz quede en la parte superior (y=0)
    y los hijos se vayan colocando abajo (y negativo).
    """
    level_dict = {}
    q = deque()
    q.append((root, 0))
    visited = set([root])
    level_dict[0] = [root]

    # BFS para separar nodos por niveles
    while q:
        current, level = q.popleft()
        for child in current.children:
            if child not in visited:
                visited.add(child)
                q.append((child, level+1))
                if (level+1) not in level_dict:
                    level_dict[level+1] = []
                level_dict[level+1].append(child)

    # Asignamos posición (x, y) para cada nodo
    pos = {}
    for level, nodes_in_level in level_dict.items():
        num_nodes = len(nodes_in_level)
        for i, node_obj in enumerate(nodes_in_level):
            x = x_factor * (i - (num_nodes - 1)/2.0)
            y = -level  # nivel 0 => y=0, nivel 1 => y=-1, etc.
            pos[node_obj.name] = (x, y)

    return pos

def plot_tree(root):
    """
    Dibuja el árbol con la raíz arriba y los hijos abajo.
    Diferencia nodos MAX (azul claro), MIN (verde claro) y podados (rojo).
    """
    G = nx.DiGraph()     # Creamos grafo dirigido
    stack = [root]
    name_to_node = {root.name: root}

    # Recorremos el árbol para añadir nodos y aristas
    while stack:
        current = stack.pop()
        G.add_node(current.name)
        for child in current.children:
            name_to_node[child.name] = child
            G.add_edge(current.name, child.name)
            stack.append(child)

    # Calculamos posición jerárquica
    pos = get_hierarchy_pos(root, x_factor=3.0)

    # Construimos etiquetas
    labels = {}
    for node_name, node_obj in name_to_node.items():
        player_str = "MAX" if node_obj.max_player else "MIN"
        val_str = "None" if node_obj.value is None else str(node_obj.value)
        labels[node_name] = f"{node_name}\n({player_str})\n(v={val_str})"

    # Definimos colores de cada nodo
    node_colors = []
    for node_name in G.nodes():
        node_obj = name_to_node[node_name]
        if node_obj.pruned:
            # nodo podado => rojo
            node_colors.append("red")
        else:
            # según sea MAX o MIN
            if node_obj.max_player:
                node_colors.append("lightblue")
            else:
                node_colors.append("lightgreen")

    # Dibujamos
    plt.figure(figsize=(16, 10))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_color=node_colors,
        node_size=2500,
        font_size=8,
        arrows=False
    )
    plt.title("Árbol Alfa-Beta con diferenciación MAX/MIN y nodos podados en rojo.")
    plt.show()

import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

class Node:
    def __init__(self, name, depth, max_player=True):
        self.name = name
        self.depth = depth
        self.max_player = max_player
        self.children = []
        self.value = None     # Valor en caso de hoja o resultado de alfa-beta
        self.pruned = False   # Indica si este nodo quedó podado

    def is_terminal(self):
        return len(self.children) == 0

    def __repr__(self):
        return (f"Node({self.name}, depth={self.depth}, "
                f"max={self.max_player}, value={self.value}, pruned={self.pruned})")


def alpha_beta(node, alpha, beta):
    if node.pruned:
        return None

    if node.is_terminal():
        return node.value

    if node.max_player:
        value = float('-inf')
        for i, child in enumerate(node.children):
            child_value = alpha_beta(child, alpha, beta)
            if child_value is not None:
                value = max(value, child_value)
                alpha = max(alpha, value)

            if alpha >= beta:
                # Marcar podados los hijos restantes
                for j in range(i+1, len(node.children)):
                    node.children[j].pruned = True
                break

        node.value = value
        return value
    else:
        value = float('inf')
        for i, child in enumerate(node.children):
            child_value = alpha_beta(child, alpha, beta)
            if child_value is not None:
                value = min(value, child_value)
                beta = min(beta, value)

            if beta <= alpha:
                # Marcar podados los hijos restantes
                for j in range(i+1, len(node.children)):
                    node.children[j].pruned = True
                break

        node.value = value
        return value


def build_tree_manual(depth, branching_factor, current_depth=0, node_name="N0", max_player=True, node_counter=[0]):
    node = Node(node_name, current_depth, max_player)
    if current_depth == depth:
        valor_str = input(f"Ingrese valor para la hoja {node_name} (profundidad {current_depth}): ")
        try:
            node.value = float(valor_str)
        except ValueError:
            print("Valor inválido. Se asigna 0 por defecto.")
            node.value = 0
        return node

    for i in range(branching_factor):
        node_counter[0] += 1
        new_name = f"N{node_counter[0]}"
        child = build_tree_manual(
            depth,
            branching_factor,
            current_depth + 1,
            node_name=new_name,
            max_player=not max_player,
            node_counter=node_counter
        )
        node.children.append(child)

    return node


def get_hierarchy_pos(root, x_factor=2.0):
    """
    Genera posiciones (x,y) para cada nodo en forma jerárquica (raíz arriba).
    - y = -level (raíz en y=0, hijos en y negativo)
    - x se reparte según la cantidad de nodos en cada nivel.
    El parámetro x_factor define cuánto separarse en X.
    """
    level_dict = {}
    q = deque()
    q.append((root, 0))
    visited = set([root])
    level_dict[0] = [root]

    while q:
        current, level = q.popleft()
        for child in current.children:
            if child not in visited:
                visited.add(child)
                q.append((child, level+1))
                if (level+1) not in level_dict:
                    level_dict[level+1] = []
                level_dict[level+1].append(child)

    pos = {}
    for level, nodes_in_level in level_dict.items():
        num_nodes = len(nodes_in_level)
        # Distribuir en X
        for i, node_obj in enumerate(nodes_in_level):
            # El factor x_factor separa más o menos
            x = x_factor * (i - (num_nodes - 1)/2.0)
            y = -level  # la raíz en y=0, luego más abajo
            pos[node_obj.name] = (x, y)

    return pos


def plot_tree(root):
    G = nx.DiGraph()
    stack = [root]
    name_to_node = {root.name: root}

    while stack:
        current = stack.pop()
        G.add_node(current.name)
        for child in current.children:
            name_to_node[child.name] = child
            G.add_edge(current.name, child.name)
            stack.append(child)

    # Calcula posiciones con un factor mayor (por ejemplo, x_factor=3.0)
    pos = get_hierarchy_pos(root, x_factor=3.0)

    labels = {}
    for node_name, node_obj in name_to_node.items():
        val_str = "None" if node_obj.value is None else str(node_obj.value)
        labels[node_name] = f"{node_name}\n(v={val_str})"

    node_colors = []
    for node_name in G.nodes():
        if name_to_node[node_name].pruned:
            node_colors.append("red")
        else:
            node_colors.append("lightgreen")

    # Ajustar tamaño de la figura (16 ancho x 10 alto)
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
    plt.title("Árbol Alfa-Beta (raíz arriba). Nodos podados en rojo.")
    plt.show()


def main():
    print("=== Construcción de un árbol para probar Alfa-Beta con la raíz en la parte superior ===")
    profundidad = int(input("Ingrese la profundidad del árbol (ej. 2): "))
    branching = int(input("Ingrese el número de hijos por nodo (ej. 2): "))

    root = build_tree_manual(depth=profundidad, branching_factor=branching)

    print("\nEjecutando Alfa-Beta...\n")
    resultado = alpha_beta(root, float('-inf'), float('inf'))
    print(f"Valor óptimo en la raíz ({root.name}): {resultado}")

    plot_tree(root)


if __name__ == "__main__":
    main()

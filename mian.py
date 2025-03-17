import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

class Node:
    def __init__(self, name, depth, max_player=True):
        self.name = name
        self.depth = depth
        self.max_player = max_player
        self.children = []
        self.value = None     # valor si es hoja o evaluación tras Alfa-Beta
        self.pruned = False   # indica si se podó este nodo

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
            # Poda
            if alpha >= beta:
                # marcamos los demás hijos como podados
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
            # Poda
            if beta <= alpha:
                # marcamos los demás hijos como podados
                for j in range(i+1, len(node.children)):
                    node.children[j].pruned = True
                break
        node.value = value
        return value

def build_tree_manual(depth, current_depth=0, node_name="N0", max_player=True, node_counter=[0]):
    """
    Ejemplo que pregunta en cada nodo cuántos hijos se desea.
    Si se elige 0 (o estamos en el nivel máximo), se pide el valor (nodo hoja).
    """
    node = Node(node_name, current_depth, max_player)

    # Si alcanzamos profundidad máxima, es hoja
    if current_depth == depth:
        val_str = input(f"Valor de la hoja {node_name} (prof. {current_depth}): ")
        try:
            node.value = float(val_str)
        except ValueError:
            print("Valor inválido. Se asigna 0.")
            node.value = 0
        return node

    # Si no es profundidad máxima, preguntamos cuántos hijos
    while True:
        try:
            cant_hijos = int(input(f"¿Cuántos hijos desea para {node_name} (prof. {current_depth})? "))
            break
        except ValueError:
            print("Por favor, ingresa un número entero.")

    if cant_hijos <= 0:
        # Es hoja => pedir valor
        val_str = input(f"Valor de la hoja {node_name}: ")
        try:
            node.value = float(val_str)
        except ValueError:
            print("Valor inválido. Se asigna 0.")
            node.value = 0
        return node
    else:
        # Creamos esos hijos
        for i in range(cant_hijos):
            node_counter[0] += 1
            new_name = f"N{node_counter[0]}"
            child = build_tree_manual(
                depth,
                current_depth + 1,
                node_name=new_name,
                max_player=not max_player,
                node_counter=node_counter
            )
            node.children.append(child)

    return node

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
        for i, node_obj in enumerate(nodes_in_level):
            x = x_factor * (i - (num_nodes - 1)/2.0)
            y = -level  # La raíz en y=0
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

    # Calculamos las posiciones
    pos = get_hierarchy_pos(root, x_factor=3.0)

    # Construimos las etiquetas incluyendo si es MAX o MIN
    labels = {}
    for node_name, node_obj in name_to_node.items():
        player_str = "MAX" if node_obj.max_player else "MIN"
        val_str = "None" if node_obj.value is None else str(node_obj.value)
        labels[node_name] = f"{node_name}\n({player_str})\n(v={val_str})"

    # Asignamos colores:
    # - Rojo si el nodo está podado.
    # - Azul claro si es MAX y no está podado.
    # - Verde claro si es MIN y no está podado.
    node_colors = []
    for node_name in G.nodes():
        node_obj = name_to_node[node_name]
        if node_obj.pruned:
            node_colors.append("red")
        else:
            if node_obj.max_player:
                node_colors.append("lightblue")
            else:
                node_colors.append("lightgreen")

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

def main():
    print("=== Construcción de un árbol donde cada nodo puede tener diferente cantidad de hijos ===")
    profundidad = int(input("Ingrese la profundidad máxima (p.ej. 2): "))

    root = build_tree_manual(depth=profundidad)

    print("\nEjecutando Alfa-Beta...\n")
    resultado = alpha_beta(root, float('-inf'), float('inf'))
    print(f"Valor óptimo en la raíz ({root.name}): {resultado}\n")

    print("Dibujando árbol...")
    plot_tree(root)

if __name__ == "__main__":
    main()

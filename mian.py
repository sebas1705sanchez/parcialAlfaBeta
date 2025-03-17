import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


class Node:
    def __init__(self, name, depth, max_player=True):
        """
        :param name: identificador del nodo, p. ej. 'N0', 'N1', etc.
        :param depth: profundidad del nodo en el árbol (0 = raíz).
        :param max_player: True si este nivel corresponde a MAX, False si corresponde a MIN.
        """
        self.name = name
        self.depth = depth
        self.max_player = max_player
        self.children = []
        self.value = None  # valor si es hoja o evaluación tras Alfa-Beta
        self.pruned = False  # indica si se podó este nodo (no evaluado)

    def is_terminal(self):
        return len(self.children) == 0

    def __repr__(self):
        return (f"Node({self.name}, depth={self.depth}, "
                f"max={self.max_player}, value={self.value}, pruned={self.pruned})")


def alpha_beta(node, alpha, beta):
    """
    Implementación del algoritmo Alfa-Beta.
    - Asigna node.value con la mejor evaluación.
    - Marca con node.pruned = True los hijos que no llegan a evaluarse (poda).
    """
    if node.pruned:
        return None

    # Si es hoja, devolvemos su valor
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
                # Marcamos el resto de hijos como podados
                for j in range(i + 1, len(node.children)):
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
                # Marcamos el resto de hijos como podados
                for j in range(i + 1, len(node.children)):
                    node.children[j].pruned = True
                break

        node.value = value
        return value


def build_tree_manual(depth, current_depth=0, node_name="N0", max_player=True, node_counter=[0]):
    """
    Construye recursivamente un árbol hasta 'depth' niveles.
    En cada nodo (si current_depth < depth):
      - Se pregunta cuántos hijos quieres darle a este nodo.
      - Si la respuesta es > 0, se crean esos hijos.
      - Si la respuesta es 0, se pide valor para nodo hoja.
    Si current_depth == depth, directamente es hoja y se pide su valor.

    :param depth: Profundidad máxima del árbol.
    :param current_depth: Profundidad actual en la recursión.
    :param node_name: Identificador del nodo.
    :param max_player: True si es turno de MAX en este nivel; False si es turno de MIN.
    :param node_counter: array de 1 elemento para asignar nombres únicos a nuevos nodos.
    :return: El nodo raíz de este subárbol.
    """
    node = Node(node_name, current_depth, max_player)

    # Si ya estamos en el nivel máximo, este nodo es hoja
    if current_depth == depth:
        valor_str = input(f"Valor de la hoja {node_name} (profundidad {current_depth}): ")
        try:
            node.value = float(valor_str)
        except ValueError:
            print("Valor inválido. Se asigna 0 por defecto.")
            node.value = 0
        return node

    # De lo contrario, preguntamos cuántos hijos quieres en este nodo
    while True:
        try:
            cant_hijos = int(input(f"¿Cuántos hijos desea para {node_name} (prof. {current_depth})? "))
            break
        except ValueError:
            print("Por favor, ingresa un número entero.")

    if cant_hijos <= 0:
        # Si no hay hijos, es hoja => pedimos su valor
        valor_str = input(f"Valor de la hoja {node_name}: ")
        try:
            node.value = float(valor_str)
        except ValueError:
            print("Valor inválido. Se asigna 0 por defecto.")
            node.value = 0
        return node
    else:
        # Creamos 'cant_hijos' nodos hijos
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
    Genera posiciones (x,y) para cada nodo en forma jerárquica (raíz arriba).
    - Realizamos un BFS para saber qué nodos hay en cada nivel.
    - y = -level  => la raíz en y=0 y los siguientes niveles en y negativo.
    - x se reparte horizontalmente para cada nivel, ampliado por x_factor.
    Retorna un diccionario: { node_name: (x, y) }
    """
    level_dict = {}
    from collections import deque
    q = deque()
    q.append((root, 0))
    visited = set([root])
    level_dict[0] = [root]

    while q:
        current, level = q.popleft()
        for child in current.children:
            if child not in visited:
                visited.add(child)
                q.append((child, level + 1))
                if (level + 1) not in level_dict:
                    level_dict[level + 1] = []
                level_dict[level + 1].append(child)

    pos = {}
    for level, nodes_in_level in level_dict.items():
        num_nodes = len(nodes_in_level)
        for i, node_obj in enumerate(nodes_in_level):
            # x_factor para regular la separación horizontal
            x = x_factor * (i - (num_nodes - 1) / 2.0)
            y = -level
            pos[node_obj.name] = (x, y)
    return pos


def plot_tree(root):
    """
    Dibuja el árbol con:
      - raíz en la parte superior (y=0)
      - nodos hijos abajo (y negativo).
    Nodos podados: rojo
    Nodos evaluados: verde claro
    """
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

    # Calcula posiciones con un factor mayor para separar más
    pos = get_hierarchy_pos(root, x_factor=3.0)

    # Etiquetas
    labels = {}
    for node_name, node_obj in name_to_node.items():
        val_str = "None" if node_obj.value is None else str(node_obj.value)
        labels[node_name] = f"{node_name}\n(v={val_str})"

    # Colores: rojo si node.pruned=True, verde claro en caso contrario
    node_colors = []
    for node_name in G.nodes():
        if name_to_node[node_name].pruned:
            node_colors.append("red")
        else:
            node_colors.append("lightgreen")

    # Dibujo con figura más grande para que no se encimen
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
    plt.title("Árbol Alfa-Beta (raíz arriba)\nNodos podados en rojo; Nodos evaluados en verde")
    plt.show()


def main():
    print("=== Construcción de un árbol con branching distinto en cada nodo ===")
    # Profundidad máxima para forzar el límite de recursión
    profundidad = int(input("Ingrese la profundidad máxima del árbol (ej. 2): "))

    # Construimos el árbol de manera manual, preguntando en cada nodo cuántos hijos desea
    root = build_tree_manual(depth=profundidad)

    print("\nEjecutando Alfa-Beta...\n")
    resultado = alpha_beta(root, float('-inf'), float('inf'))
    print(f"Valor óptimo en la raíz ({root.name}): {resultado}\n")

    print("Dibujando árbol...")
    plot_tree(root)


if __name__ == "__main__":
    main()

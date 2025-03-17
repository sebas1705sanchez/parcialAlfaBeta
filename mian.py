import matplotlib.pyplot as plt
import networkx as nx

class Node:
    def __init__(self, name, depth, max_player=True):
        """
        :param name: identificador del nodo (por ejemplo, "N0", "N1", etc.)
        :param depth: la profundidad del nodo en el árbol (0 = raíz).
        :param max_player: True si este nivel corresponde a MAX, False si corresponde a MIN.
        """
        self.name = name
        self.depth = depth
        self.max_player = max_player
        self.children = []
        self.value = None   # Sólo se asigna si es nodo hoja o si lo queremos forzar

    def is_terminal(self):
        return len(self.children) == 0

    def __repr__(self):
        return f"Node({self.name}, value={self.value}, max={self.max_player})"

def alpha_beta(node, alpha, beta):
    """
    Algoritmo Alfa-Beta básico sin límite de profundidad adicional,
    asumiendo que el árbol ya está construido hasta los estados terminales.
    """
    if node.is_terminal():
        # Si es hoja, devolvemos su valor directamente
        return node.value

    if node.max_player:
        value = float('-inf')
        for child in node.children:
            value = max(value, alpha_beta(child, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # poda
        node.value = value  # Se puede almacenar la evaluación en el nodo
        return value
    else:
        value = float('inf')
        for child in node.children:
            value = min(value, alpha_beta(child, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break  # poda
        node.value = value
        return value

def build_tree_manual(depth, branching_factor, current_depth=0, node_name="N0", max_player=True, node_counter=[0]):
    """
    Construye un árbol de forma recursiva hasta 'depth' niveles.
    - depth: profundidad total deseada (0 = sólo raíz).
    - branching_factor: cuántos hijos por nodo (si deseas igual para todos).
    - current_depth: profundidad actual en la recursión.
    - node_name: nombre identificador para este nodo.
    - max_player: True si en este nivel le toca a MAX, False si le toca a MIN.
    - node_counter: array de 1 elemento para llevar la cuenta de nodos creados.
    """
    node = Node(node_name, current_depth, max_player)

    # Si llegamos a la profundidad deseada, preguntamos valor al usuario (nodo hoja)
    if current_depth == depth:
        valor_str = input(f"Ingrese valor para la hoja {node_name} (profundidad {current_depth}): ")
        try:
            node.value = float(valor_str)
        except ValueError:
            print("Valor inválido. Se asignará 0 por defecto.")
            node.value = 0
        return node

    # Si no es hoja, creamos hijos
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

def plot_tree(root):
    """
    Genera un grafo con NetworkX y lo dibuja con matplotlib.
    Cada nodo queda etiquetado con su nombre y valor final (después de Alfa-Beta).
    """
    G = nx.Graph()

    # Haremos un recorrido BFS o DFS para añadir nodos y aristas
    stack = [root]
    while stack:
        current = stack.pop()
        # Añadimos el nodo (etiquetamos con: nombre y valor final)
        label = f"{current.name}\n(v={current.value})"
        G.add_node(current.name, label=label)
        # Añadimos los hijos
        for child in current.children:
            stack.append(child)
            G.add_edge(current.name, child.name)

    # Extraemos etiquetas
    labels = nx.get_node_attributes(G, 'label')

    # Dibujamos el grafo
    pos = nx.spring_layout(G)  # Calcula posición de cada nodo
    nx.draw(G, pos, with_labels=True, labels=labels)
    plt.title("Árbol con valores tras Alfa-Beta")
    plt.show()

def main():
    print("=== Construcción de un árbol para probar Alfa-Beta ===")
    # Pedimos al usuario la profundidad (0 = solo raíz con valor, 1 = raíz con hojas, etc.)
    profundidad = int(input("Ingrese la profundidad del árbol (ej. 2): "))
    branching = int(input("Ingrese el número de hijos por nodo (ej. 2): "))

    # Construimos el árbol
    root = build_tree_manual(depth=profundidad, branching_factor=branching)

    # Aplicamos Alfa-Beta
    print("\nCalculando resultado Alfa-Beta...\n")
    resultado = alpha_beta(root, float('-inf'), float('inf'))

    print(f"Valor óptimo calculado en la raíz ({root.name}): {resultado}")

    # Graficamos el árbol
    plot_tree(root)

if __name__ == "__main__":
    main()

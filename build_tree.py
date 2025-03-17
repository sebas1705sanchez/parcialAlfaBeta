# build_tree.py

from my_node import Node

def build_tree_manual(depth, current_depth=0, node_name="N0", max_player=True, node_counter=[0]):
    """
    Construye el árbol de forma recursiva hasta 'depth'.
    En cada nodo, se pregunta cuántos hijos se desea.
    Si se elige 0 o estamos en nivel máximo, se pide el valor de la hoja.
    """
    # Crea el nodo actual
    node = Node(node_name, current_depth, max_player)

    # Caso: alcanzamos la profundidad máxima => es hoja
    if current_depth == depth:
        val_str = input(f"Valor de la hoja {node_name} (prof. {current_depth}): ")
        try:
            node.value = float(val_str)
        except ValueError:
            print("Valor inválido. Se asigna 0.")
            node.value = 0
        return node

    # Si no estamos en la profundidad máxima, pedimos la cantidad de hijos
    while True:
        try:
            cant_hijos = int(input(f"¿Cuántos hijos desea para {node_name} (prof. {current_depth})? "))
            break
        except ValueError:
            print("Por favor, ingresa un número entero.")

    if cant_hijos <= 0:
        # Este nodo se convierte en hoja => valor
        val_str = input(f"Valor de la hoja {node_name}: ")
        try:
            node.value = float(val_str)
        except ValueError:
            print("Valor inválido. Se asigna 0.")
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

# alpha_beta.py

def alpha_beta(node, alpha, beta):
    """
    Implementa el algoritmo Alfa-Beta.
    - Recibe un nodo (arbol/subárbol),
    - Retorna el valor óptimo calculado.
    - Marca como podados los hijos que no se evalúan por cumplir la condición de corte.
    """
    # Si el nodo ya está marcado como podado, no se evalúa
    if node.pruned:
        return None

    # Si es un nodo terminal (hoja), devolvemos su valor
    if node.is_terminal():
        return node.value

    # CASO MAX
    if node.max_player:
        value = float('-inf')
        for i, child in enumerate(node.children):
            child_value = alpha_beta(child, alpha, beta)
            if child_value is not None:
                value = max(value, child_value)
                alpha = max(alpha, value)

            if alpha >= beta:
                # Poda: marcar hijos restantes como podados
                for j in range(i+1, len(node.children)):
                    node.children[j].pruned = True
                break

        node.value = value
        return value
    # CASO MIN
    else:
        value = float('inf')
        for i, child in enumerate(node.children):
            child_value = alpha_beta(child, alpha, beta)
            if child_value is not None:
                value = min(value, child_value)
                beta = min(beta, value)

            if beta <= alpha:
                # Poda: marcar hijos restantes como podados
                for j in range(i+1, len(node.children)):
                    node.children[j].pruned = True
                break

        node.value = value
        return value

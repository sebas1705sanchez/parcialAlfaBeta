# my_node.py

class Node:
    """
    Representa un nodo dentro del árbol de juego.
    """
    def __init__(self, name, depth, max_player=True):
        self.name = name
        self.depth = depth
        self.max_player = max_player
        self.children = []
        self.value = None    # valor si es hoja o resultado de Alfa-Beta
        self.pruned = False  # indica si este nodo se podó

    def is_terminal(self):
        """
        Retorna True si el nodo es una hoja (no tiene hijos).
        """
        return len(self.children) == 0

    def __repr__(self):
        return (f"Node({self.name}, depth={self.depth}, "
                f"max={self.max_player}, value={self.value}, pruned={self.pruned})")

# my_node.py

"""
Este archivo solo contiene la definicion de la calse Node
"""

class Node:
    """
    Representa un nodo dentro del árbol de juego.
    """
    def __init__(self, name, depth, max_player=True):
        self.name = name # Identidica el nodo
        self.depth = depth # Profundidad del arbol y de cada nodo
        self.max_player = max_player # nivel Max o Min
        self.children = [] # lista Nodos hijos
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

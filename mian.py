# main.py

from build_tree import build_tree_manual
from alpha_beta import alpha_beta
from plot_utils import plot_tree

def main():
    print("=== Construcción de un árbol donde cada nodo puede tener diferente cantidad de hijos ===")
    profundidad = int(input("Ingrese la profundidad máxima (p.ej. 2): "))

    # Construimos el árbol
    root = build_tree_manual(depth=profundidad)

    # Ejecutamos Alfa-Beta
    print("\nEjecutando Alfa-Beta...\n")
    resultado = alpha_beta(root, float('-inf'), float('inf'))
    print(f"Valor óptimo en la raíz ({root.name}): {resultado}\n")

    # Graficamos
    print("Dibujando árbol...")
    plot_tree(root)


if __name__ == "__main__":
    main()

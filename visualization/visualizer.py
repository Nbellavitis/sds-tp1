import matplotlib.patches as patches
import sys

def parse_static(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    l = float(lines[1].strip())
    radii = []
    for line in lines[2:2+n]:
        parts = line.split()
        radii.append(float(parts[0]))
    return n, l, radii

def parse_dynamic(filepath, n):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    positions = []
    for line in lines[1:1+n]:
        parts = line.split()
        positions.append((float(parts[0]), float(parts[1])))
    return positions

def parse_neighbors(filepath):
    neighbors = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip().strip('[]')
            parts = line.split()
            if not parts:
                continue
            p_id = int(parts[0])
            n_ids = [int(x) for x in parts[1:]]
            neighbors[p_id] = n_ids
    return neighbors

import glob
import os

def main():
    if len(sys.argv) == 3:
        ts = sys.argv[1]
        target_id = int(sys.argv[2])
    else:
        ts = input("Ingrese el timestamp: ")
        target_id = int(input("Ingrese el ID de la particula foco: "))

    # Buscar el archivo de output que contiene el rc en el nombre
    output_pattern = f'data/{ts}-rc-*-output.txt'
    matched_files = glob.glob(output_pattern)

    if not matched_files:
        print(f"Error: No se encontro el archivo de vecinos para el timestamp {ts}.")
        sys.exit(1)

    output_filepath = matched_files[0]

    # Extraer el valor de rc limpiando el nombre del archivo
    filename = os.path.basename(output_filepath)
    rc_str = filename.split('-rc-')[1].replace('-output.txt', '')
    rc = float(rc_str)

    print(f"-> Radio de corte (rc) detectado automaticamente: {rc}")

    n, l, radii = parse_static(f'data/{ts}.txt')
    positions = parse_dynamic(f'data/{ts}-Dynamic.txt', n)
    neighbors = parse_neighbors(output_filepath)

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, l)
    ax.set_ylim(0, l)
    ax.set_aspect('equal')

    target_neighbors = neighbors.get(target_id, [])
    target_x, target_y, target_r = 0, 0, 0

    for i in range(n):
        p_id = i + 1
        x, y = positions[i]
        r = radii[i]

        if p_id == target_id:
            color = 'green'
            zorder = 3
            target_x, target_y, target_r = x, y, r
            ax.text(x, y, str(p_id), fontsize=9, ha='center', va='center', zorder=4, color='white', fontweight='bold')
        elif p_id in target_neighbors:
            color = 'blue'
            zorder = 2
            ax.text(x, y, str(p_id), fontsize=8, ha='center', va='center', zorder=4, color='white')
        else:
            color = 'lightgray'
            zorder = 1

        circle = patches.Circle((x, y), radius=r, facecolor=color, edgecolor='black', zorder=zorder, alpha=0.7)
        ax.add_patch(circle)

    if target_r > 0:
        interaction_radius = target_r + rc
        rc_circle = patches.Circle((target_x, target_y), radius=interaction_radius, fill=False, edgecolor='red', linestyle='--', linewidth=1.5, zorder=5, label=f'Área de interacción (rc={rc})')
        ax.add_patch(rc_circle)
        ax.legend(loc='upper right')

    plt.title(f"Sistema de Particulas (Timestamp: {ts}) - Foco: {target_id} - N: {n}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

if __name__ == "__main__":
    main()
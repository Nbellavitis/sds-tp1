import matplotlib.patches as patches
import matplotlib.pyplot as plt
import sys
import glob
import os

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

def main():
    if len(sys.argv) == 3:
        ts = sys.argv[1]
        target_id = int(sys.argv[2])
    else:
        ts = input("Ingrese el timestamp: ")
        target_id = int(input("Ingrese el ID de la particula foco: "))

    output_pattern = f'data/{ts}-rc-*-output.txt'
    matched_files = glob.glob(output_pattern)

    if not matched_files:
        print(f"Error: No se encontro el archivo de vecinos para el timestamp {ts}.")
        sys.exit(1)

    output_filepath = matched_files[0]

    filename = os.path.basename(output_filepath)
    periodic = '-periodic-' in filename or filename.endswith('-periodic-output.txt')
    rc_str = filename.split('-rc-')[1].replace('-periodic-output.txt', '').replace('-output.txt', '')
    rc = float(rc_str)

    print(f"-> Radio de corte (rc) detectado automaticamente: {rc}")
    print(f"-> Condiciones periodicas: {'Si' if periodic else 'No'}")

    n, l, radii = parse_static(f'data/{ts}.txt')
    positions = parse_dynamic(f'data/{ts}-Dynamic.txt', n)
    neighbors = parse_neighbors(output_filepath)

    target_neighbors = neighbors.get(target_id, [])
    target_x, target_y, target_r = 0.0, 0.0, 0.0

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_xlim(0, l)
    ax.set_ylim(0, l)

    # ── Box boundary ──────────────────────────────────────────────────────────
    box = patches.Rectangle((0, 0), l, l, linewidth=2,
                             edgecolor='black', facecolor='none', zorder=10)
    ax.add_patch(box)

    # ── Clip path: everything outside the box is invisible ───────────────────
    # We create a clip rectangle in data coordinates.
    clip_rect = patches.Rectangle((0, 0), l, l, transform=ax.transData)

    # ── Draw particles ────────────────────────────────────────────────────────
    particle_circles = []   # (patch, label_text) tuples for label management
    label_objects = []

    for i in range(n):
        p_id = i + 1
        x, y = positions[i]
        r = radii[i]

        if p_id == target_id:
            color = 'green'
            zorder = 3
            target_x, target_y, target_r = x, y, r
        elif p_id in target_neighbors:
            color = 'blue'
            zorder = 2
        else:
            color = 'lightgray'
            zorder = 1

        circle = patches.Circle((x, y), radius=r,
                                 facecolor=color, edgecolor='black',
                                 zorder=zorder, alpha=0.7)
        circle.set_clip_path(clip_rect)
        ax.add_patch(circle)
        particle_circles.append(circle)

        # Labels – drawn but visibility toggled dynamically on zoom
        lbl = ax.text(x, y, str(p_id),
                      fontsize=7, ha='center', va='center',
                      zorder=zorder + 1,
                      color='white' if color != 'lightgray' else 'dimgray',
                      fontweight='bold' if p_id == target_id else 'normal',
                      visible=False)
        lbl.set_clip_path(clip_rect)
        label_objects.append((lbl, r))

    # ── Interaction circle(s) ─────────────────────────────────────────────────
    if target_r > 0:
        interaction_radius = target_r + rc
        if periodic:
            offsets = [0, -l, l]
            first = True
            for dx in offsets:
                for dy in offsets:
                    cx, cy = target_x + dx, target_y + dy
                    if (cx + interaction_radius >= 0 and cx - interaction_radius <= l and
                            cy + interaction_radius >= 0 and cy - interaction_radius <= l):
                        label = f'Área de interacción (rc={rc}, periódico)' if first else None
                        rc_circle = patches.Circle((cx, cy), radius=interaction_radius,
                                                   fill=False, edgecolor='red',
                                                   linestyle='--', linewidth=1.5,
                                                   zorder=5, label=label)
                        rc_circle.set_clip_path(clip_rect)
                        ax.add_patch(rc_circle)
                        first = False
        else:
            rc_circle = patches.Circle((target_x, target_y), radius=interaction_radius,
                                       fill=False, edgecolor='red',
                                       linestyle='--', linewidth=1.5, zorder=5,
                                       label=f'Área de interacción (rc={rc})')
            rc_circle.set_clip_path(clip_rect)
            ax.add_patch(rc_circle)
        ax.legend(loc='upper right')

    # ── Dynamic label visibility on zoom/pan ─────────────────────────────────
    # Labels appear only when the particle diameter is >= MIN_LABEL_PX pixels.
    MIN_LABEL_PX = 12  # pixels
    _updating_labels = [False]  # mutable flag to prevent re-entrant calls

    def update_labels(event=None):
        if _updating_labels[0]:
            return
        _updating_labels[0] = True
        try:
            fig_width_px = fig.get_size_inches()[0] * fig.dpi
            xlim = ax.get_xlim()
            view_width = xlim[1] - xlim[0]
            if view_width <= 0:
                return
            px_per_unit = fig_width_px / view_width
            for lbl, r in label_objects:
                lx, ly = lbl.get_position()
                inside_box = (0 <= lx <= l) and (0 <= ly <= l)
                diameter_px = 2 * r * px_per_unit
                lbl.set_visible(inside_box and diameter_px >= MIN_LABEL_PX)
        finally:
            _updating_labels[0] = False

    fig.canvas.mpl_connect('draw_event', update_labels)

    # ── Scroll-wheel zoom ─────────────────────────────────────────────────────
    ZOOM_FACTOR = 1.06  # gentle step per scroll tick

    def on_scroll(event):
        if event.inaxes != ax:
            return
        cx, cy = event.xdata, event.ydata
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        factor = 1 / ZOOM_FACTOR if event.button == 'up' else ZOOM_FACTOR
        # Zoom toward the cursor: keep the point under the cursor fixed
        ax.set_xlim(cx + (xlim[0] - cx) * factor,
                    cx + (xlim[1] - cx) * factor)
        ax.set_ylim(cy + (ylim[0] - cy) * factor,
                    cy + (ylim[1] - cy) * factor)
        update_labels()
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('scroll_event', on_scroll)

    plt.title(f"Sistema de Particulas (Timestamp: {ts}) - Foco: {target_id} - N: {n}" +
              (" [Periódico]" if periodic else ""))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
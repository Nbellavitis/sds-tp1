import subprocess
import matplotlib.pyplot as plt
import random
import math
import os

def generate_temp_particles(N, L, r, static_path, dynamic_path):
    """Genera N particulas aleatorias sin superponerse y las guarda en disco."""
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    particles = []

    while len(particles) < N:
        x = random.uniform(r, L - r)
        y = random.uniform(r, L - r)
        overlap = False

        for px, py in particles:
            dist = math.sqrt((x - px)**2 + (y - py)**2)
            if dist < 2 * r:
                overlap = True
                break

        if not overlap:
            particles.append((x, y))

    with open(static_path, 'w') as f:
        f.write(f"{N}\n{L}\n")
        for _ in range(N):
            f.write(f"{r} 1.0\n")

    with open(dynamic_path, 'w') as f:
        f.write("0\n")
        for p in particles:
            f.write(f"{p[0]} {p[1]} 0.0 0.0\n")

def main():
    N = 1000
    L = 20.0
    rc = 1.0
    r = 0.25

    periodic = input("Condiciones periodicas (1 o 0): ")

    max_M = int(L / (rc + 2 * r))
    m_values = list(range(1, max_M + 1))
    times = []

    static_file = "data/temp_static.txt"
    dynamic_file = "data/temp_dynamic.txt"

    print("Compilando el proyecto...")
    subprocess.run(["mvn", "-f", "engine/pom.xml", "clean", "compile"], capture_output=True)

    print(f"Generando mapa base de N={N} particulas (esto se hace solo una vez)...")
    generate_temp_particles(N, L, r, static_file, dynamic_file)

    print("Ejecutando variaciones de M...")
    for m in m_values:
        result = subprocess.run(
            ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.Simulation",
             str(N), str(L), str(rc), str(r), str(m), periodic, "CIM", static_file, dynamic_file],
            capture_output=True, text=True
        )
        tiempo = float(result.stdout.strip())
        times.append(tiempo)
        print(f"M = {m} -> {tiempo} ms")

    plt.plot(m_values, times, marker='o')
    plt.title("Tiempo de ejecucion vs M")
    plt.xlabel("M")
    plt.ylabel("Tiempo (ms)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
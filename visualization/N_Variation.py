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
    L = 20.0
    rc = 1.0
    r = 0.25
    M = int(L / (rc + 2 * r))

    periodic = input("Condiciones periodicas (1 o 0): ")

    # Usamos valores tolerables para que no haya un bucle infinito por falta de espacio
    n_values = [100, 250, 500, 750, 1000]

    cim_times = []
    bf_times = []

    static_file = "data/temp_static.txt"
    dynamic_file = "data/temp_dynamic.txt"

    print("Compilando el proyecto...")
    subprocess.run(["mvn", "-f", "engine/pom.xml", "clean", "compile"], capture_output=True)

    for n in n_values:
        print(f"\n======= N = {n} =======")
        print("Generando mapa de particulas...")
        generate_temp_particles(n, L, r, static_file, dynamic_file)

        print("Midiendo el tiempo con Cell Index Method...")
        res_cim = subprocess.run(
            ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.Simulation",
             str(n), str(L), str(rc), str(r), str(M), periodic, "CIM", static_file, dynamic_file],
            capture_output=True, text=True
        )
        tiempo_cim = float(res_cim.stdout.strip())
        cim_times.append(tiempo_cim)
        print(f"CIM se ejecuto en {tiempo_cim} ms")

        print("Midiendo el tiempo con Fuerza Bruta...")
        res_bf = subprocess.run(
            ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.Simulation",
             str(n), str(L), str(rc), str(r), str(M), periodic, "BF", static_file, dynamic_file],
            capture_output=True, text=True
        )
        tiempo_bf = float(res_bf.stdout.strip())
        bf_times.append(tiempo_bf)
        print(f"Fuerza Bruta se ejecuto en {tiempo_bf} ms")

    plt.plot(n_values, cim_times, marker='o', label="Cell Index Method")
    plt.plot(n_values, bf_times, marker='x', label="Fuerza Bruta")
    plt.title("Tiempo de ejecucion vs N")
    plt.xlabel("N")
    plt.ylabel("Tiempo (ms)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
import subprocess
import matplotlib.pyplot as plt

def main():
    N = 1000
    L = 20.0
    rc = 1.0
    r = 0.25

    periodic = input("Condiciones periodicas (1 o 0): ")

    print("Compilando el proyecto...")
    subprocess.run(["mvn", "-f", "engine/pom.xml", "clean", "compile"], capture_output=True)

    print(f"Ejecutando variaciones de M en Java para N={N}...")
    # Llamamos a Java UNA sola vez
    res = subprocess.run(
        ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.VariationM",
         str(N), str(L), str(rc), str(r), periodic],
        capture_output=True, text=True
    )

    m_values = []
    times = []

    # Procesamos la salida de Java
    for line in res.stdout.strip().split('\n'):
        try:
            m_str, t_str = line.split()
            m_values.append(int(m_str))
            times.append(float(t_str))
            print(f"M = {m_str} -> {t_str} ms")
        except ValueError:
            continue

    plt.plot(m_values, times, marker='o', color='green')
    plt.title(f"Tiempo de ejecucion vs M (N={N})")
    plt.xlabel("M")
    plt.ylabel("Tiempo (ms)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
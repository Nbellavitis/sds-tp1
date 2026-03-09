import subprocess
import matplotlib.pyplot as plt

def main():
    N = 1000
    L = 20.0
    rc = 1.0
    r = 0.25

    periodic = input("Condiciones periodicas (1 o 0): ")

    max_M = int(L / (rc + 2 * r))
    m_values = list(range(1, max_M + 1))
    times = []

    subprocess.run(["mvn", "-f", "engine/pom.xml", "clean", "compile"])

    print("Ejecutando variaciones de M...")
    for m in m_values:
        result = subprocess.run(
            ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.Simulation",
             str(N), str(L), str(rc), str(r), str(m), periodic, "CIM"],
            capture_output=True, text=True
        )
        times.append(float(result.stdout.strip()))

    plt.plot(m_values, times, marker='o')
    plt.title("Tiempo de ejecucion vs M")
    plt.xlabel("M")
    plt.ylabel("Tiempo (ms)")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
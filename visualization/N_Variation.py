import subprocess
import matplotlib.pyplot as plt

def main():
    L = 20.0
    rc = 1.0
    r = 0.25
    M = int(L / (rc + 2 * r))

    periodic = input("Condiciones periodicas (1 o 0): ")
    n_values = [100, 250, 500, 750, 1000]

    cim_times = []
    bf_times = []

    subprocess.run(["mvn", "-f", "engine/pom.xml", "clean", "compile"])

    print("Ejecutando variaciones de N...")
    for n in n_values:
        res_cim = subprocess.run(
            ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.Simulation",
             str(n), str(L), str(rc), str(r), str(M), periodic, "CIM"],
            capture_output=True, text=True
        )
        cim_times.append(float(res_cim.stdout.strip()))

        res_bf = subprocess.run(
            ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.Simulation",
             str(n), str(L), str(rc), str(r), str(M), periodic, "BF"],
            capture_output=True, text=True
        )
        bf_times.append(float(res_bf.stdout.strip()))

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
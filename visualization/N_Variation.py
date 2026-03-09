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

    print("Compilando el proyecto...")
    subprocess.run(["mvn", "-f", "engine/pom.xml", "clean", "compile"], capture_output=True)

    for n in n_values:
        print(f"\n======= N = {n} =======")

        res = subprocess.run(
            ["java", "-cp", "engine/target/classes", "ar.edu.itba.sds.VariationN",
             str(n), str(L), str(rc), str(r), str(M), periodic],
            capture_output=True, text=True
        )

        try:
            t_cim_str, t_bf_str = res.stdout.strip().split()
            tiempo_cim = float(t_cim_str)
            tiempo_bf = float(t_bf_str)

            cim_times.append(tiempo_cim)
            bf_times.append(tiempo_bf)

            print(f"CIM se ejecuto en {tiempo_cim} ms")
            print(f"Fuerza Bruta se ejecuto en {tiempo_bf} ms")
        except ValueError:
            print(f"Error: {res.stdout}")

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
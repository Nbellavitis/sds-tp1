# TP1 - Simulación de Sistemas

El presente trabajo implementa y analiza el algoritmo **Cell Index
Method (CIM)** para detectar vecinos en sistemas de partículas
bidimensionales, desarrollado en el marco de la materia **Simulación de
Sistemas** del **Instituto Tecnológico de Buenos Aires (ITBA)**.

El objetivo principal es comparar su desempeño contra una solución de
**fuerza bruta**, evaluar el impacto de distintos parámetros y generar
visualizaciones de las configuraciones resultantes.

El cálculo de distancias entre partículas se realiza **de borde a
borde**, y el sistema soporta simulaciones tanto con **condiciones de
contorno periódicas** como **no periódicas (paredes rígidas)**.

La arquitectura del proyecto es híbrida:

-   **Java 17 + Maven** como motor de cálculo de alta performance.
-   **Python 3** como orquestador para la ejecución de pruebas, análisis
    de datos y generación de gráficos.

------------------------------------------------------------------------

## Funcionalidades Incluidas

-   **Método de Cell Index**\
    Construye una grilla `MxM` para acelerar la detección de partículas
    vecinas en un área de lado `L`.

-   **Referencia de Fuerza Bruta**\
    Calcula los vecinos sin optimizaciones (comparando todos los pares
    posibles) para validar resultados y medir diferencias de
    performance.

-   **Análisis de Desempeño**\
    Ejecuta experimentos variando la cantidad de celdas y partículas,
    midiendo tiempos de ejecución y generando curvas comparativas.

-   **Visualización**\
    Produce archivos de salida estandarizados y grafica la configuración
    del sistema, destacando la partícula foco, sus vecinos y el radio de
    corte.

------------------------------------------------------------------------

## Requisitos Previos

Para ejecutar el proyecto es necesario contar con:

-   Java 17 (o superior)
-   Maven
-   Python 3.10 (o superior)
-   pip

------------------------------------------------------------------------

## Instalación y Configuración

Clonar el repositorio y navegar a la carpeta raíz del proyecto:

``` bash
git clone <tu-repositorio-url>
cd sds-tp1
```

Crear un entorno virtual para Python y activarlo:

``` bash
python3 -m venv venv
source venv/bin/activate
```

Instalar las dependencias de visualización:

``` bash
pip install matplotlib
```

Compilar el motor de cálculo en Java:

``` bash
./compile.sh
```

------------------------------------------------------------------------

## Manual de Usuario

Todos los comandos deben ejecutarse **desde la raíz del repositorio con
el entorno virtual activado**.

------------------------------------------------------------------------

## Simulación Principal

Ejecuta el motor de simulación.\
El script solicitará los siguientes parámetros por consola:

N: cantidad de partículas a generar.\
L: longitud del lado de la grilla cuadrada.\
r_c: radio de interacción para considerar vecinos.\
r: radio de cada partícula.\
M: cantidad de celdas por eje (debe cumplir M ≤ L / (r_c + 2r)).\
periodic: 1 para activar contorno periódico, 0 para contorno abierto.

Si se corre sin argumentos, utilizará los archivos de prueba ubicados en
la carpeta `data/`.

``` bash
./run.sh
```

Al finalizar, se crearán tres archivos bajo el directorio `data/` con un
prefijo de timestamp:

-   Estado estático
-   Estado dinámico (`-Dynamic.txt`)
-   Lista de vecinos (`-output.txt`)

------------------------------------------------------------------------

## Visualización de Resultados

Permite graficar una simulación previamente calculada.

``` bash
python3 visualization/Visualizer.py
```

El script solicitará:

-   El timestamp de la corrida
-   El ID de la partícula
-   El radio de corte (`rc`)

Luego mostrará un gráfico 2D con la partícula foco resaltada y sus
vecinos.

------------------------------------------------------------------------

## Performance variando M

Analiza el impacto de la cantidad de celdas en la grilla manteniendo
fija la cantidad de partículas.

``` bash
python3 visualization/M_Variation.py
```

El script: 1. Compilará el código 2. Recorrerá todos los valores válidos
de `M` 3. Graficará la curva de tiempos de ejecución

------------------------------------------------------------------------

## Performance variando N

Compara los tiempos de ejecución del **Cell Index Method** contra el
método de **Fuerza Bruta** a medida que aumenta el volumen del sistema.

``` bash
python3 visualization/N_Variation.py
```

El script: 1. Generará partículas aleatorias para distintos valores de
`N` 2. Ejecutará ambos algoritmos 3. Mostrará las curvas comparativas
para visualizar la mejora de rendimiento.

import csv
import numpy as np
import statistics as stats
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# ========= CONFIGURACIÓN ==========
CARPETA_DATOS = r"D:\PIA_ProgBas\PIA_PrograBas\Guardar_datos"
CARPETA_GRAFICAS = r"D:\PIA_ProgBas\PIA_PrograBas\graficas"
# ==================================

# Solicitar ciudad
def solicitar_ciudad():
    return input("Ingrese el nombre de la ciudad (ej. monterrey, cdmx): ").strip().lower()

# Validar archivo
def validar_archivo(ciudad):
    carpeta_ciudad = os.path.join(CARPETA_DATOS, ciudad, "csv")
    archivo_csv = os.path.join(carpeta_ciudad, f"datos_{ciudad}.csv")
    if not os.path.exists(archivo_csv):
        print(f"No se encontró el archivo para la ciudad '{ciudad}'.")
        return None
    return archivo_csv

# Leer el CSV y extraer datos numéricos
def leer_datos(archivo_csv):
    datos_contaminantes = defaultdict(list)
    with open(archivo_csv, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            for contaminante in ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]:
                try:
                    valor = float(fila[contaminante])
                    datos_contaminantes[contaminante].append(valor)
                except ValueError:
                    continue
    return datos_contaminantes

# Resumen estadístico
def resumen_estadistico(nombre, datos):
    print(f"\n {nombre.upper()}")
    print(f" - Media: {np.mean(datos):.2f}")
    print(f" - Mediana: {np.median(datos):.2f}")
    try:
        moda = stats.mode(datos)
        print(f" - Moda: {moda:.2f}")
    except:
        print(" - Moda: No definida o múltiple")
    print(f" - Desviación estándar: {np.std(datos):.2f}")
    print(f" - Mínimo: {np.min(datos):.2f}")
    print(f" - Máximo: {np.max(datos):.2f}")

# Generar gráficas
def generar_graficas(datos, ciudad):
    carpeta_graficas_ciudad = os.path.join(CARPETA_GRAFICAS, ciudad)
    os.makedirs(carpeta_graficas_ciudad, exist_ok=True)
    for contaminante, valores in datos.items():
        if valores:
            plt.figure()
            plt.plot(valores, label=contaminante, marker='o')
            plt.title(f"Gráfico de Línea - {contaminante.upper()} en {ciudad.capitalize()}")
            plt.xlabel("Índice de Registro")
            plt.ylabel("Concentración")
            plt.grid()
            plt.legend()
            archivo_grafica = os.path.join(carpeta_graficas_ciudad, f"grafica_{contaminante}_{ciudad}.png")
            plt.savefig(archivo_grafica)
            plt.close()
            print(f"Gráfica guardada en: {archivo_grafica}")

# Main
def main():
    ciudad = solicitar_ciudad()
    archivo_csv = validar_archivo(ciudad)
    if not archivo_csv:
        return
    datos = leer_datos(archivo_csv)
    for contaminante, valores in datos.items():
        if valores:
            resumen_estadistico(contaminante, valores)
    generar_graficas(datos, ciudad)

if __name__ == "__main__":
    main()

import csv
import numpy as np
import statistics as stats
from collections import defaultdict
import os

# ========= CONFIGURACIÓN ==========
CARPETA = r"D:\PIA_ProgBas\PIA_PrograBas\Guardar_datos"
# ==================================

# Solicitar ciudad
ciudad = input("Ingrese el nombre de la ciudad (ej. monterrey, cdmx): ").strip().lower()
archivo_csv = os.path.join(CARPETA, f"datos_{ciudad}.csv")

# Validar existencia del archivo
if not os.path.exists(archivo_csv):
    print(f"No se encontró el archivo para la ciudad '{ciudad}'. Verifica que exista '{archivo_csv}'")
    exit()

# Inicializar estructura
datos_contaminantes = defaultdict(list)

# Leer el CSV y extraer datos numéricos
with open(archivo_csv, newline='', encoding='utf-8') as f:
    lector = csv.DictReader(f)
    for fila in lector:
        for contaminante in ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]:
            try:
                valor = float(fila[contaminante])
                datos_contaminantes[contaminante].append(valor)
            except ValueError:
                continue

# Función de análisis estadístico
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
    print(f" - Rango: {np.ptp(datos):.2f}")

# Ejecutar análisis
print(f"\n Estadísticas para la ciudad: {ciudad.upper()}")
for contaminante, valores in datos_contaminantes.items():
    if valores:
        resumen_estadistico(contaminante, valores)
    else:
        print(f"\nNo hay datos válidos para '{contaminante}'.")

# Diccionario útil para visualización futura
datos_para_visualizacion = dict(datos_contaminantes)
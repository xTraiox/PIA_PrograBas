import csv
import re
import os

def validar_fila(fila):
    """
    Validación de datos con expresiones regulares y reglas lógicas:
    - ciudad: solo letras y espacios
    - fecha_hora: formato YYYY-MM-DD HH:MM:SS
    - AQI: número del 1 al 5
    - Contaminantes: números enteros o decimales positivos
    """
    errores = []

    # Validar ciudad
    if not re.match(r"^[a-záéíóúñ\s]+$", fila["ciudad"], re.IGNORECASE):
        errores.append("Ciudad inválida")

    # Validar fecha_hora
    if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", fila["fecha_hora"]):
        errores.append("Formato de fecha/hora inválido")

    # Validar AQI
    if not re.match(r"^[1-5]$", fila["aqi"]):
        errores.append("AQI inválido")

    # Validar valores numéricos de contaminantes
    contaminantes = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]
    for c in contaminantes:
        if not re.match(r"^\d+(\.\d+)?$", fila[c]):
            errores.append(f"{c.upper()} no es numérico")

    return errores

def leer_csv(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"El archivo {ruta_archivo} no existe.")
        return

    print(f"\nValidando archivo: {ruta_archivo}\n")

    with open(ruta_archivo, mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        fila_num = 1
        for fila in lector:
            errores = validar_fila(fila)
            if errores:
                print(f"Fila {fila_num} inválida: {errores}")
            else:
                print(f"Fila {fila_num} válida")
            fila_num += 1

def main():
    archivo = input("📂 Nombre del archivo CSV a validar (ej: datos_monterrey.csv): ").strip()
    leer_csv(archivo)

if __name__ == "__main__":
    main()

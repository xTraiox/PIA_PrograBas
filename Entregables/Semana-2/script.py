import requests
import re
import json
import csv
import os
from datetime import datetime

API_KEY = '21d1855f81c6b624b91ca2580ea5b172'
URL_BASE = 'http://api.openweathermap.org/data/2.5/air_pollution'
CARPETA_DATOS = r"D:\PIA_ProgBas\PIA_PrograBas\Guardar_datos"  # Ruta absoluta

# Diccionario de ciudades
ciudades = {
    "monterrey": (25.6866, -100.3161),
    "cdmx": (19.4326, -99.1332),
    "guadalajara": (20.6597, -103.3496),
    "puebla": (19.0414, -98.2063)
}

def validar_ciudad(ciudad):
    patron = re.compile(r"^[a-zA-Záéíóúñ\s]+$", re.IGNORECASE)
    return bool(patron.match(ciudad))

def consultar_calidad_aire(ciudad):
    ciudad = ciudad.lower()
    if ciudad in ciudades:
        lat, lon = ciudades[ciudad]
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY
        }
        respuesta = requests.get(URL_BASE, params=params)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"Error en la consulta: {respuesta.status_code}")
            return None
    else:
        print("Ciudad no encontrada en la base de datos.")
        return None

def limpiar_datos(json_data, ciudad):
    try:
        resultado = []
        for item in json_data["list"]:
            data_limpia = {
                "ciudad": ciudad.lower(),
                "fecha_hora": datetime.utcfromtimestamp(item["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
                "aqi": item["main"]["aqi"],
                "co": item["components"]["co"],
                "no": item["components"]["no"],
                "no2": item["components"]["no2"],
                "o3": item["components"]["o3"],
                "so2": item["components"]["so2"],
                "pm2_5": item["components"]["pm2_5"],
                "pm10": item["components"]["pm10"],
                "nh3": item["components"]["nh3"]
            }
            resultado.append(data_limpia)
        return resultado
    except KeyError as e:
        print(f"Error al limpiar datos: campo faltante - {e}")
        return []

def guardar_datos_csv(datos, ciudad):
    # Crear la carpeta si no existe
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)

    nombre_csv = os.path.join(CARPETA_DATOS, f"datos_{ciudad.lower()}.csv")
    nombre_txt = os.path.join(CARPETA_DATOS, f"datos_{ciudad.lower()}.txt")
    campos = ["ciudad", "fecha_hora", "aqi", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]

    archivo_existente = os.path.exists(nombre_csv)
    modo = 'a' if archivo_existente else 'w'

    with open(nombre_csv, mode=modo, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        if not archivo_existente:
            writer.writeheader()
        writer.writerows(datos)

    print(f"Datos estructurados guardados como {nombre_csv}")

    with open(nombre_txt, mode='a', encoding='utf-8') as f:
        for fila in datos:
            f.write(json.dumps(fila, ensure_ascii=False) + '\n')

    print(f"Datos también guardados como {nombre_txt}")

def main():
    ciudad_input = input("Ingresa el nombre de la ciudad a consultar: ").strip()

    if not validar_ciudad(ciudad_input):
        print("Nombre de ciudad inválido. Solo letras y espacios permitidos.")
        return

    datos_json = consultar_calidad_aire(ciudad_input)

    if datos_json:
        # Crear la carpeta si no existe
        if not os.path.exists(CARPETA_DATOS):
            os.makedirs(CARPETA_DATOS)

        nombre_json = os.path.join(CARPETA_DATOS, f"datos_{ciudad_input.lower()}.json")
        with open(nombre_json, "w", encoding="utf-8") as archivo:
            json.dump(datos_json, archivo, indent=4, ensure_ascii=False)
        print(f"JSON original guardado como {nombre_json}")

        datos_limpios = limpiar_datos(datos_json, ciudad_input)
        if datos_limpios:
            guardar_datos_csv(datos_limpios, ciudad_input)
        else:
            print("No se pudieron limpiar los datos.")

if __name__ == "__main__":
    main()

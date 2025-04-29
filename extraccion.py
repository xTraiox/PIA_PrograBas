import requests
import re
import json

API_KEY = '21d1855f81c6b624b91ca2580ea5b172'
URL_BASE = 'http://api.openweathermap.org/data/2.5/air_pollution'

# Diccionario de ciudades
ciudades = {
    "monterrey": (25.6866, -100.3161),
    "cdmx": (19.4326, -99.1332),
    "guadalajara": (20.6597, -103.3496),
    "puebla": (19.0414, -98.2063)
}

def validar_ciudad(ciudad):
    """Valida que la ciudad solo contenga letras"""
    patron = re.compile(r"^[a-zA-Záéíóúñ\s]+$", re.IGNORECASE)
    return bool(patron.match(ciudad))

def consultar_calidad_aire(ciudad):
    """Consulta la calidad del aire de una ciudad válida"""
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

def main():
    ciudad_input = input("Ingresa el nombre de la ciudad a consultar: ").strip()
    
    # Validar con regex
    if not validar_ciudad(ciudad_input):
        print("Nombre de ciudad inválido. Solo letras y espacios permitidos.")
        return
    
    datos = consultar_calidad_aire(ciudad_input)
    
    if datos:
        with open(f"datos_{ciudad_input.lower()}.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print(f"Datos guardados correctamente en datos_{ciudad_input.lower()}.json")

if __name__ == "__main__":
    main()

import requests
import re

API_KEY = '21d1855f81c6b624b91ca2580ea5b172'

# Diccionario con coordenadas de ciudades
ciudades = {
    "monterrey": (25.6866, -100.3161),
    "cdmx": (19.4326, -99.1332),
    "guadalajara": (20.6597, -103.3496),
    "puebla": (19.0414, -98.2063),
    "tijuana": (32.5149, -117.0382)
}

def validar_ciudad(nombre):
    patron = r"^[a-zA-ZáéíóúñÑ\s]+$"
    return re.match(patron, nombre.strip().lower())

# Solicitar entrada del usuario
entrada = input("Ingresa el nombre de la ciudad: ").strip().lower()

if not validar_ciudad(entrada):
    print("Nombre inválido. Usa solo letras y espacios.")
    exit()

if entrada not in ciudades:
    print("Ciudad no encontrada en la base. Intenta con: Monterrey, CDMX, Guadalajara, Puebla, Tijuana")
    exit()

lat, lon = ciudades[entrada]

url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    aqi = data['list'][0]['main']['aqi']
    pm2_5 = data['list'][0]['components']['pm2_5']
    pm10 = data['list'][0]['components']['pm10']

    print(f"\n Ciudad: {entrada.title()}")
    print(f"Índice de Calidad del Aire (AQI): {aqi} (1=bajo, 5=alto)")
    print(f"PM2.5: {pm2_5} µg/m³")
    print(f"PM10: {pm10} µg/m³")
else:
    print("Error al consultar la API:", response.status_code)

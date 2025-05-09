import os

def ejecutar_script(script):
    os.system(f'python D:\\PIA_ProgBas\\PIA_PrograBas\\{script}')



def menu():
    while True:
        print("\n=== Menú de Scripts ===")
        print("1. Análisis de Gráficas")
        print("2. Exportar a Excel")
        print("3. Extracción y Limpieza")
        print("4. Lectura y Validación de Calidad del Aire")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ejecutar_script("analisis_graficas.py")
        elif opcion == "2":
            ejecutar_script("exportar_excel.py")
        elif opcion == "3":
            ejecutar_script("extraccion_limpieza.py")
        elif opcion == "4":
            ejecutar_script("lectura_validacion_calidad_aire.py")
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()

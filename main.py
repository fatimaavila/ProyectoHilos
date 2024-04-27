# import os
# import time
# import numpy as np
# import csv
# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# from datetime import datetime

# def calcular_estadisticas(datos):
#     media = np.mean(datos)
#     desviacion_estandar = np.std(datos)
#     conteo = len(datos)
#     valor_minimo = np.min(datos)
#     valor_maximo = np.max(datos)
#     return media, desviacion_estandar, conteo, valor_minimo, valor_maximo

# def procesar_csv(archivo_csv):
#     # Leer datos del archivo CSV
#     with open(archivo_csv, 'r') as f:
#         reader = csv.reader(f)
#         next(reader)  # Saltar la primera fila (encabezado)
#         datos = [float(row[0]) for row in reader]

#     # Calcular estadísticas
#     estadisticas = calcular_estadisticas(datos)

#     # Escribir resultados en un archivo
#     nombre_archivo_salida = f"resultado_{os.path.basename(archivo_csv)}"
#     with open(nombre_archivo_salida, 'w') as f:
#         f.write("Media, Desviación Estándar, Conteo, Mínimo, Máximo\n")
#         f.write(",".join(map(str, estadisticas)))

#     return nombre_archivo_salida

# def convertir_a_fecha(fecha_str):
#     return datetime.strptime(fecha_str, '%Y-%m-%d')
# def main():
#     # Configuración de archivos y parámetros
    
#     archivo_csv = "datos.csv"  # Nombre del archivo CSV
#     modelos_paralelismo = [...]  # Lista de modelos de paralelismo a probar
#     num_iteraciones = 10

#     # Procesamiento
#     resultados = {}
#     for modelo in modelos_paralelismo:
#         resultados[modelo] = []
#         for _ in range(num_iteraciones):
#             tiempo_inicial = time.time()

#             # Ejecutar en paralelo según el modelo
#             with ThreadPoolExecutor() as executor:  # o ProcessPoolExecutor para procesamiento basado en procesos
#                 archivos_procesados = list(executor.map(procesar_csv, [archivo_csv] * 1000))  # Cambiar 1000 por el número de archivos

#             tiempo_final = time.time()
#             tiempo_total = tiempo_final - tiempo_inicial
#             resultados[modelo].append(tiempo_total)

#     # Guardar resultados de tiempo en un archivo
#     with open("resultados_tiempo.csv", 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(["Modelo", "Tiempo Promedio (segundos)"])
#         for modelo, tiempos in resultados.items():
#             tiempo_promedio = sum(tiempos) / len(tiempos)
#             writer.writerow([modelo, tiempo_promedio])

# if __name__ == "__main__":
#     main()


import os
import time
import numpy as np
import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def calcular_estadisticas(datos):
    # Convertir fechas a timestamps (números)
    timestamps = [date.timestamp() for date in datos]
    media = np.mean(timestamps)
    desviacion_estandar = np.std(timestamps)
    conteo = len(datos)
    valor_minimo = np.min(timestamps)
    valor_maximo = np.max(timestamps)
    
    # Convertir de nuevo a objetos datetime para el resultado
    fecha_minima = datetime.fromtimestamp(valor_minimo)
    fecha_maxima = datetime.fromtimestamp(valor_maximo)
    
    return media, desviacion_estandar, conteo, fecha_minima, fecha_maxima

def convertir_a_fecha(fecha_str):
    return datetime.strptime(fecha_str, '%Y/%m/%d')

def procesar_csv(archivo_csv):
    # Leer datos del archivo CSV
    with open(archivo_csv, 'r') as f:
        reader = csv.DictReader(f)
        datos = [convertir_a_fecha(row['dates']) for row in reader]

    # Calcular estadísticas
    estadisticas = calcular_estadisticas(datos)

    # Escribir resultados en un archivo
    nombre_archivo_salida = f"resultado_{os.path.basename(archivo_csv)}"
    with open(nombre_archivo_salida, 'w') as f:
        f.write("Media, Desviación Estándar, Conteo, Mínimo, Máximo\n")
        f.write(",".join(map(str, estadisticas)))

    return nombre_archivo_salida

def main():
    # Configuración de archivos y parámetros
    archivo_csv = "datos.csv"  # Nombre del archivo CSV
    modelos_paralelismo = [...]  # Lista de modelos de paralelismo a probar
    num_iteraciones = 10

    # Procesamiento
    resultados = {}
    for modelo in modelos_paralelismo:
        resultados[modelo] = []
        for _ in range(num_iteraciones):
            tiempo_inicial = time.time()

            # Ejecutar en paralelo según el modelo
            with ThreadPoolExecutor() as executor:
                archivos_procesados = list(executor.map(procesar_csv, [archivo_csv] * 1000))  # Cambiar 1000 por el número de archivos

            tiempo_final = time.time()
            tiempo_total = tiempo_final - tiempo_inicial  # Corrección aquí
            resultados[modelo].append(tiempo_total)

    # Guardar resultados de tiempo en un archivo
    with open("resultados_tiempo.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Modelo", "Tiempo Promedio (segundos)"])
        for modelo, tiempos in resultados.items():
            tiempo_promedio = sum(tiempos) / len(tiempos)
            writer.writerow([modelo, tiempo_promedio])

if __name__ == "__main__":
    main()


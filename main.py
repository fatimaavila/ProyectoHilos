# import os
# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import time
# import numpy as np
# from multiprocessing import cpu_count
# # path donde esta la data
# INPUT_DIR = '../ProyectoHiloss/so_data'



# def list_files(directory):
#     files = os.listdir(directory)
#     print("Files in directory:")
#     for file in files:
#         print(file)

# # ver que si estenleyendose los files
# list_files(INPUT_DIR)


# def calculate_stats(data):
#     # datos estadisticos
#     numeric_data = data.select_dtypes(include=[np.number])
#     return {
#         'count': numeric_data.count(),
#         'mean': numeric_data.mean(),
#         'std': numeric_data.std(),
#         'min': numeric_data.min(),
#         'max': numeric_data.max()
#     }

# def process_file(file_path):
#     # Process a single file and save stats
#     data = pd.read_csv(file_path)
#     stats = calculate_stats(data)
#     output_filename = f"{os.path.splitext(file_path)[0]}_out.csv"
#     pd.DataFrame(stats).to_csv(output_filename, index=False)
#     return output_filename

# def run_sequential(input_dir):
#     # Run all files sequentially
#     start_time = time.time()
#     for filename in os.listdir(input_dir):
#         if filename.endswith('.csv') and not filename.endswith('_out.csv'):
#             process_file(os.path.join(input_dir, filename))
#     return time.time() - start_time

# def run_parallel_files(input_dir, max_workers):
#     # Run file processing in parallel
#     start_time = time.time()
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = [executor.submit(process_file, os.path.join(input_dir, filename))
#                    for filename in os.listdir(input_dir)
#                    if filename.endswith('.csv') and not filename.endswith('_out.csv')]
#         for future in as_completed(futures):
#             future.result()  # Wait for each file to be processed
#     return time.time() - start_time

# def main():
#     # Adjust max_workers based on the threading model and CPU core/thread restrictions
#     threading_models = {
#         '1core-1thread': 1,
#         '1core-4threads': 4,
#         '2core-2threads': 2,
#         '2core-4threads': 4,
#         '2core-8threads': 8,
#         '4core-8threads': 8  # You need to ensure your system has 4 cores available for this
#     }
    
#     all_results = {}

#     for model_name, max_workers in threading_models.items():
#         print(f"Running model: {model_name}")
#         time_results = []
#         for _ in range(10):  # Perform 10 iterations
#             start_time = time.time()
#             results = run_parallel_files(INPUT_DIR, max_workers)
#             end_time = time.time()
#             time_taken = end_time - start_time
#             time_results.append(time_taken)
#         all_results[model_name] = time_results

#     # Save all timing results to a single CSV file
#     df = pd.DataFrame.from_dict(all_results)
#     df.to_csv('c:/Users/Javier C/OneDrive - Universidad Francisco Marroquin/Clases/Sistemas operativos/ProyectoHiloss/time_results.csv', index=False)

# if __name__ == "__main__":
#     main()

import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Ruta donde está la data
INPUT_DIR = "../ProyectoHiloss/so_data"


def calculate_stats_threaded(data, threads):
    # Calcular estadísticas en hilos
    def get_count():
        return data.count()

    def get_mean():
        return data.mean(numeric_only=True)

    def get_std():
        return data.std(ddof=1, numeric_only=True)

    def get_min():
        return data.min(numeric_only=True)

    def get_max():
        return data.max(numeric_only=True)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_stat = {
            executor.submit(get_count): "count",
            executor.submit(get_mean): "mean",
            executor.submit(get_std): "std",
            executor.submit(get_min): "min",
            executor.submit(get_max): "max",
        }
        stats = {}
        for future in as_completed(future_to_stat):
            stat_name = future_to_stat[future]
            stats[stat_name] = future.result()
    return stats


def calculate_stats_sequential(data):
    # Calcular estadísticas de forma secuencial
    stats = {
        "count": data.count(),
        "mean": data.mean(numeric_only=True),
        "std": data.std(ddof=1, numeric_only=True),
        "min": data.min(numeric_only=True),
        "max": data.max(numeric_only=True),
    }
    return stats


def process_file_threaded(file_path, threads):
    # Procesar un solo archivo y guardar las estadísticas de forma paralela
    data = pd.read_csv(file_path)
    stats = calculate_stats_sequential(data)
    output_filename = f"{os.path.splitext(file_path)[0]}_out.csv"
    pd.DataFrame(stats).to_csv(output_filename, index=False)
    return output_filename


def process_file_sequential(file_path, threads):
    # Procesar un solo archivo y guardar las estadísticas de forma secuencial
    data = pd.read_csv(file_path)
    stats = calculate_stats_threaded(data, threads)
    output_filename = f"{os.path.splitext(file_path)[0]}_out.csv"
    pd.DataFrame(stats).to_csv(output_filename, index=False)
    return output_filename


def run_files_sequential(input_dir, threads):
    # Procesar archivos secuencialmente
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv") and not filename.endswith("_out.csv"):
            process_file_sequential(os.path.join(input_dir, filename), threads)


def run_files_parallel(input_dir, threads):
    # Procesar archivos en paralelo
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for filename in os.listdir(input_dir):
            if filename.endswith(".csv") and not filename.endswith("_out.csv"):
                file_path = os.path.join(input_dir, filename)
                futures.append(
                    executor.submit(process_file_threaded, file_path, threads)
                )
        for future in as_completed(futures):
            future.result()


def main():
    print("Elige el modo de ejecución:")
    print("1. Procesamiento de archivos secuencial y funciones paralelas")
    print("2. Procesamiento de archivos paralelos y funciones secuenciales")
    choice = int(input("Ingrese el número de opción: "))

    if choice == 1:
        print("Elige el número de hilos para ejecutar:")
        print("1. 1 hilo")
        print("2. 2 hilos")
        print("3. 4 hilos")
        print("4. 8 hilos")
        choice = int(input("Ingrese el número de opción: "))

        if choice == 1:
            threads = 1
        elif choice == 2:
            threads = 2
        elif choice == 3:
            threads = 4
        elif choice == 4:
            threads = 8
        else:
            print("Opción no válida. Saliendo del programa.")
            return

        start_time = time.time()
        run_files_sequential(INPUT_DIR, threads)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Tiempo total de ejecución: {total_time:.2f} segundos")
    elif choice == 2:
        print("Elige el número de hilos para ejecutar:")
        print("1. 1 hilo")
        print("2. 2 hilos")
        print("3. 4 hilos")
        print("4. 8 hilos")
        choice = int(input("Ingrese el número de opción: "))
        if choice == 1:
            threads = 1
        elif choice == 2:
            threads = 2
        elif choice == 3:
            threads = 4
        elif choice == 4:
            threads = 8
        else:
            print("Opción no válida. Saliendo del programa.")
            return

        start_time = time.time()
        run_files_parallel(INPUT_DIR, threads)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Tiempo total de ejecución: {total_time:.2f} segundos")
    else:
        print("Opción no válida. Saliendo del programa.")


if __name__ == "__main__":
    main()
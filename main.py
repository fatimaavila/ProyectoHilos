import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import argparse

# Ruta donde está la data
# INPUT_DIR = "../ProyectoHiloss/so_data"
INPUT_DIR = "/app/so_data"

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
    stats = calculate_stats_threaded(data, threads)
    output_filename = f"{os.path.splitext(file_path)[0]}_out.csv"
    pd.DataFrame(stats).to_csv(output_filename, index=False)
    return output_filename

def process_file_sequential(file_path):
    # Procesar un solo archivo y guardar las estadísticas de forma secuencial
    data = pd.read_csv(file_path)
    stats = calculate_stats_sequential(data)
    output_filename = f"{os.path.splitext(file_path)[0]}_out.csv"
    pd.DataFrame(stats).to_csv(output_filename, index=False)
    return output_filename

def run_files_sequential(input_dir, threads):
    # Procesar archivos secuencialmente
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv") and not filename.endswith("_out.csv"):
            process_file_threaded(os.path.join(input_dir, filename), threads)

def run_files_parallel(input_dir, threads):
    # Procesar archivos en paralelo
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for filename in os.listdir(input_dir):
            if filename.endswith(".csv") and not filename.endswith("_out.csv"):
                file_path = os.path.join(input_dir, filename)
                futures.append(
                    executor.submit(process_file_sequential, file_path)
                )
        for future in as_completed(futures):
            future.result()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=int, help='Modo de ejecución (1 o 2)')
    parser.add_argument('threads', type=int, help='Número de hilos para usar')
    args = parser.parse_args()
    if args.mode == 1:
        start_time = time.time()
        run_files_sequential(INPUT_DIR, args.threads)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Tiempo total de ejecución: {total_time:.2f} segundos")
    elif args.mode == 2:
        start_time = time.time()
        run_files_parallel(INPUT_DIR, args.threads)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Tiempo total de ejecución: {total_time:.2f} segundos")
    else:
        print("Opción no válida. Saliendo del programa.")

if __name__ == "__main__":
    main()

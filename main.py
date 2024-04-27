import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import numpy as np
from multiprocessing import cpu_count
# Define the path for the directory where the CSV files are located

INPUT_DIR = '../Proy3/so_data'



def list_files(directory):
    files = os.listdir(directory)
    print("Files in directory:")
    for file in files:
        print(file)

# Call the list_files function before running the main function
list_files(INPUT_DIR)


def calculate_stats(data):
    # Select only numeric data for statistics calculations
    numeric_data = data.select_dtypes(include=[np.number])
    return {
        'count': numeric_data.count(),
        'mean': numeric_data.mean(),
        'std': numeric_data.std(),
        'min': numeric_data.min(),
        'max': numeric_data.max()
    }

def process_file(file_path):
    # Process a single file and save stats
    data = pd.read_csv(file_path)
    stats = calculate_stats(data)
    output_filename = f"{os.path.splitext(file_path)[0]}_out.csv"
    pd.DataFrame(stats).to_csv(output_filename, index=False)
    return output_filename

def run_sequential(input_dir):
    # Run all files sequentially
    start_time = time.time()
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv') and not filename.endswith('_out.csv'):
            process_file(os.path.join(input_dir, filename))
    return time.time() - start_time

def run_parallel_files(input_dir, max_workers):
    # Run file processing in parallel
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, os.path.join(input_dir, filename))
                   for filename in os.listdir(input_dir)
                   if filename.endswith('.csv') and not filename.endswith('_out.csv')]
        for future in as_completed(futures):
            future.result()  # Wait for each file to be processed
    return time.time() - start_time

def main():
    # Adjust max_workers based on the threading model and CPU core/thread restrictions
    threading_models = {
        '1core-1thread': 1,
        '1core-4threads': 4,
        '2core-2threads': 2,
        '2core-4threads': 4,
        '2core-8threads': 8,
        '4core-8threads': 8  # You need to ensure your system has 4 cores available for this
    }
    
    time_results = {}

    # Get the actual number of cores for demonstration purposes
    available_cores = cpu_count()
    print(f"Available cores: {available_cores}")

    for model_name, max_workers in threading_models.items():
        print(f"Running model: {model_name}")
        time_results[model_name] = []
        for _ in range(10):  # Perform 10 iterations
            if model_name == 'sequential':
                time_taken = run_sequential(INPUT_DIR)
            else:
                time_taken = run_parallel_files(INPUT_DIR, max_workers)
            time_results[model_name].append(time_taken)
        
        # Output results for this model
        avg_time = np.mean(time_results[model_name])
        print(f"{model_name} took an average of {avg_time:.2f} seconds per run over 10 iterations")

    # Save the timing results to a CSV file
    pd.DataFrame.from_dict(time_results, orient='index').to_csv('../Proy3/so_data/time_results.csv')

if __name__ == "__main__":
    main()
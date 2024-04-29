#!/bin/bash

run_program() {
    mode=$1
    cores=$2
    threads=$3
    echo "Ejecutando contenedor en modo $mode con $cores núcleos y $threads hilos..."
    execution_output=$(docker run -m 1g --cpus $cores -e CPU_LIMIT=$cores --rm --name proyecto-hilos proyecto-hilos $mode $threads | grep "Tiempo total de ejecución")
    execution_time=$(echo $execution_output | cut -d ' ' -f 5)
    echo "Tiempo de ejecución: $execution_time segundos"
    echo "$mode, $cores, $threads, $execution_time" >> execution_times.csv
}

echo "Modo, Cores, Hilos, Tiempo de Ejecución (segundos)" > execution_times.csv

for mode in 1 2; do
    for cores in 1 2 4; do
        if [ $cores -eq 1 ]; then
            for threads in 1 4; do
                run_program $mode $cores $threads
            done
        elif [ $cores -eq 2 ]; then
            for threads in 2 4 8; do
                run_program $mode $cores $threads
            done
        elif [ $cores -eq 4 ]; then
            for threads in 8; do
                run_program $mode $cores $threads
            done
        fi
    done
done

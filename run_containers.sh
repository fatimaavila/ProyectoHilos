#!/bin/bash
declare -a configs=(
    "1 1 1"   # 1 core, 1 hilo
    "1 4 1"   # 1 core, 4 hilos
    "2 2 2"   # 2 cores, 2 hilos
    "2 4 2"   # 2 cores, 4 hilos
    "2 8 2"   # 2 cores, 8 hilos
    "4 8 4"   # 4 cores, 8 hilos
)

# Bucle para iterar sobre cada configuración
for config in "${configs[@]}"
do
    IFS=' ' read -r -a array <<< "$config"
    cores="${array[2]}"
    threads="${array[1]}"
    mode=1  # Ejecutar primero en modo 1

    echo "Ejecutando contenedor en modo $mode con $cores núcleos y $threads hilos..."
    docker run -m 1g --cpus $cores -e CPU_LIMIT=$cores --rm --name proyecto-hilos proyecto-hilos $mode $threads

    mode=2  # Ejecutar luego en modo 2

    echo "Ejecutando contenedor en modo $mode con $cores núcleos y $threads hilos..."
    docker run -m 1g --cpus $cores -e CPU_LIMIT=$cores --rm --name proyecto-hilos proyecto-hilos $mode $threads

done

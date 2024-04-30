# Proyecto Hilos 🧵

Este proyecto consiste en un script en Python diseñado para procesar archivos CSV y calcular estadísticas sobre los datos contenidos en estos archivos. 

El script proporciona opciones para realizar el procesamiento de manera secuencial o en paralelo, lo que permite aprovechar al máximo los recursos de hardware disponibles, como el número de núcleos de CPU y el número de hilos.

Se incluyen dos modos de ejecución: 
- Modo secuencial
- Modo paralelo

Con la capacidad de especificar el número de hilos a utilizar en el modo paralelo. Además, se proporciona funcionalidad para realizar múltiples ejecuciones del script con diferentes configuraciones de CPU, permitiendo evaluar el rendimiento en varios escenarios. 

## Línea para correrlo en Docker 🐳

``` docker run -m 1g --cpus 1 -e CPU_LIMIT=1 --rm --name proyecto-hilos proyecto-hilos 1 1 ```

- cpus cambia el número de cores
- El último parámetro cambia el número de hilos



### [Informe XLS con estadísticas 📊](https://docs.google.com/spreadsheets/d/1GAxQcifyXMgTyCkSgWlbltlQT4QfHTmAWHnQnPSuRvs/edit?usp=sharing)

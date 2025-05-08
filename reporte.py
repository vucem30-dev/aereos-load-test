"""
Resumen de resultados JMeter (.jtl)

Este script procesa un archivo .jtl generado por JMeter para producir un resumen
estadístico útil para reportes ejecutivos.

INSTRUCCIONES DE USO:

1. Asegúrate de haber corrido tu prueba JMeter en modo no-GUI usando algo como:
   jmeter -n -t files/test.jmx -q files/test.properties -l results/results.jtl

2. Coloca este script en la misma carpeta del archivo .jtl, o ajusta la ruta en 'file_path'.

3. Ejecuta el script con:
   python3 -m venv env
   source env/bin/activate  # Linux/Mac
   python3 -m pip install --upgrade pip
   pip install numpy
   pip freeze > requirements.txt
   python3 resumen.py

4. Verás en consola un resumen como este:
   - Solicitudes totales
   - Tiempo promedio y máximo de respuesta
   - Porcentaje de éxito
   - Throughput
   - Tiempo de conexión promedio
   - Errores HTTP 500 y 400
   - Métricas adicionales (latencia, desviación estándar, percentiles, etc.)
"""

import csv
import statistics
import numpy as np

# Ruta al archivo .jtl
file_path = 'results/results.jtl'

with open(file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

total_requests = len(rows)
elapsed_times = [int(row['elapsed']) for row in rows]
connect_times = [int(row['Connect']) for row in rows]
latency_times = [int(row['Latency']) for row in rows if row['Latency'].isdigit()]
thread_names = set(row['threadName'] for row in rows)

success_count = sum(1 for row in rows if row['success'] == 'true')
http_500 = sum(1 for row in rows if row['responseCode'].startswith('500'))
http_400 = sum(1 for row in rows if row['responseCode'].startswith('400'))

first_ts = int(rows[0]['timeStamp'])
last_ts = int(rows[-1]['timeStamp'])

# Métricas base
duration_sec = (last_ts - first_ts) / 1000
avg_elapsed_sec = statistics.mean(elapsed_times) / 1000
max_elapsed_sec = max(elapsed_times) / 1000
avg_connect_ms = statistics.mean(connect_times)
throughput = total_requests / duration_sec
success_rate = (success_count / total_requests) * 100

# Métricas adicionales
std_elapsed_sec = statistics.stdev(elapsed_times) / 1000 if len(elapsed_times) > 1 else 0
median_elapsed_sec = statistics.median(elapsed_times) / 1000
p90 = np.percentile(elapsed_times, 90) / 1000
p95 = np.percentile(elapsed_times, 95) / 1000
p99 = np.percentile(elapsed_times, 99) / 1000
avg_latency_ms = sum(latency_times) / len(latency_times) if latency_times else 0
max_threads = max(int(row['allThreads']) for row in rows)

# Mostrar resultados
print(f"Solicitudes totales:\t{total_requests:,}")
print(f"Tiempo promedio respuesta:\t{avg_elapsed_sec:.2f} segundos")
print(f"Tiempo máximo respuesta:\t{max_elapsed_sec:.2f} segundos")
print(f"Porcentaje de éxito:\t{success_rate:.1f}%")
print(f"Throughput:\t{throughput:.1f} transacciones/seg")
print(f"Tiempo de conexión promedio:\t{avg_connect_ms:.0f} ms")
print(f"Errores HTTP 500:\t{http_500}")
print(f"Errores HTTP 400:\t{http_400}")
print(f"Duración de la prueba:\t{duration_sec:.2f} segundos")
print(f"Fecha de inicio:\t{rows[0]['timeStamp']}")
print(f"Fecha de fin:\t{rows[-1]['timeStamp']}")

# Extras
print(f"Desviación estándar respuesta:\t{std_elapsed_sec:.2f} segundos")
print(f"Mediana tiempo respuesta:\t{median_elapsed_sec:.2f} segundos")
print(f"Percentil 90:\t{p90:.2f} s")
print(f"Percentil 95:\t{p95:.2f} s")
print(f"Percentil 99:\t{p99:.2f} s")
print(f"Latencia promedio:\t{avg_latency_ms:.0f} ms")
print(f"Usuarios virtuales únicos:\t{len(thread_names)}")
print(f"Máxima concurrencia:\t{max_threads} threads")

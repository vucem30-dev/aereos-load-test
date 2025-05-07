#!/bin/bash
set -e

# Crea el directorio si no existe
mkdir -p files/results/html_report

# Ejecuta JMeter
/opt/jmeter/bin/jmeter -n \
  -t files/test.jmx \
  -q files/test.properties \
  -l files/results/results.jtl \
  -e -o files/results/html_report

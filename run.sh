#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Ejecutando con parametros por defecto (N=100, L=100, rc=6, r=0.37, M=13, periodic=1)..."
    java -cp engine/target/classes ar.edu.itba.sds.Simulation 100 100 6 0.37 13 1 CIM
else
    echo "Ejecutando con parametros personalizados..."
    java -cp engine/target/classes ar.edu.itba.sds.Simulation "$@"
fi
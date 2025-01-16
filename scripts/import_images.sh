#!/bin/bash
#Descripción: Script para enviar imágenes almacenadas en los .tar al cluster k3s

# Script para importar imágenes tar en k3s

# Guardar las imágenes de Docker en archivos tar sin sobrescribir
echo "Guardando las imágenes de Docker en archivos tar..."
[ ! -f tokensrv.tar ] && docker save -o tokensrv.tar tokensrv
[ ! -f authsrv.tar ] && docker save -o authsrv.tar authsrv
[ ! -f service.tar ] && docker save -o service.tar service

# Lista de archivos tar a importar
imagenes=("tokensrv.tar" "authsrv.tar" "service.tar")

# Importar cada imagen
for imagen in "${imagenes[@]}"; do
    echo "Importando $imagen..."
    sudo k3s ctr images import "$imagen"
    if [ $? -eq 0 ]; then
        echo "$imagen importada exitosamente."
    else
        echo "Error al importar $imagen."
    fi
done

echo "Todas las imágenes han sido importadas."
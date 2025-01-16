#!/bin/bash

#Descripción: Script para enviar imágenes de Docker a un nodo remoto y luego importarlas en k3s
#Ejemplo: ./send_images.sh user@remote_host /path/to/destination

# Nodo de destino
DEST_NODE=$1

# Directorio de destino en el nodo remoto
DEST_DIR=$2

# Verificar si se proporcionaron los argumentos necesarios
if [ -z "$DEST_NODE" ] || [ -z "$DEST_DIR" ]; then
  echo "Uso: $0 <nodo_destino> <directorio_destino>"
  echo "Ejemplo: $0 user@remote_host /path/to/destination"
  exit 1
fi

# Crear un directorio temporal llamado temp en el directorio actual

mkdir -p temp


# Guardar las imágenes de Docker en archivos tar sin sobrescribir
echo "Guardando las imágenes de Docker en archivos tar..."
[ ! -f tokensrv.tar ] && docker save -o temp/tokensrv.tar tokensrv
[ ! -f authsrv.tar ] && docker save -o temp/authsrv.tar authsrv
[ ! -f service.tar ] && docker save -o temp/service.tar service

# Mover los archivos tar al directorio actual
mv $TEMP_DIR/*.tar .

# Copiar los archivos tar al nodo de destino
echo "Copiando los archivos tar al nodo de destino..."
scp tokensrv.tar $DEST_NODE:$DEST_DIR
scp authsrv.tar $DEST_NODE:$DEST_DIR
scp service.tar $DEST_NODE:$DEST_DIR

# Importar las imágenes en el nodo de destino
echo "Importando las imágenes en el nodo de destino..."
ssh $DEST_NODE "sudo k3s ctr images import $DEST_DIR/tokensrv.tar"
ssh $DEST_NODE "sudo k3s ctr images import $DEST_DIR/authsrv.tar"
ssh $DEST_NODE "sudo k3s ctr images import $DEST_DIR/service.tar"

# Limpiar el directorio temporal
rm -rf temp

echo "Imágenes importadas exitosamente en el nodo $DEST_NODE"
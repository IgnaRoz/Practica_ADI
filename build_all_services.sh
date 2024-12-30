#!/bin/bash

# Build and delete token service repo
echo "Clonando el repositorio del servicio de tokens..."
git clone https://github.com/IgnaRoz/apiREST.git token_service_rep
cd token_service_rep
echo "Instalando dependencias del servicio de tokens..."
pip install .
echo "Construyendo el servicio de tokens..."
./build.sh
cd ..
echo "Eliminando el repositorio del servicio de tokens..."
rm -rf token_service_rep

# Build and delete authentication repo
echo "Clonando el repositorio del servicio de autenticación..."
git clone --branch entregable2 https://github.com/luideoz/Authentication.git adi_auth_srv_rep
export STORAGE_FOLDER="storage"
cd adi_auth_srv_rep
echo "Instalando dependencias del servicio de autenticación..."
pip install .
echo "Iniciando el servicio de autenticación..."
python3 bootstrap.py
echo "Construyendo el servicio de autenticación..."
./build.sh
cd ..
echo "Eliminando el repositorio del servicio de autenticación..."
rm -rf adi_auth_srv_rep

# Build and delete blob service repo
echo "Clonando el repositorio del servicio de blobs..."
git clone --branch main https://github.com/SergiooCoorne/Blob_Service_ADI.git blob_service_rep
cd blob_service_rep
echo "Construyendo el servicio de blobs..."
./scripts/build.sh
cd ..
echo "Eliminando el repositorio del servicio de blobs..."
rm -rf blob_service_rep
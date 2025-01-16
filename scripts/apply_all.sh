#!/bin/bash

# Aplicar todos los archivos YAML en el directorio srv
kubectl apply -f srv/

# Instala  el controlador(modificado como nodeport) nginx para el ingress
#kubectl apply -f ingress/ingress-nginx-deploy.yaml

# Instala el controlador(sin modificar) nginx para el ingress
#kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud/deploy.yaml

# Aplicar el archivo de configuración del ingress
kubectl apply -f ingress/ingress.yaml
kubectl apply -f ingress/ingress-service.yaml #Es el servicio que se encarga de redirigir el trafico al ingress y expone un puerto para que se pueda acceder desde el exterior

# Aplicar archivos específicos en el directorio volumenes
kubectl apply -f volumenes/pv_blob_test.yaml
kubectl apply -f volumenes/pv_auth_test.yaml
kubectl apply -f volumenes/pvc_auth.yaml
kubectl apply -f volumenes/pvc__blob.yaml
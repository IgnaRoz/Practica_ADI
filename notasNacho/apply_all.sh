#!/bin/bash

# Aplicar todos los archivos YAML en el directorio srv
kubectl apply -f srv/

# Aplicar todos los archivos YAML en el directorio ingress
kubectl apply -f ingress/

# Aplicar archivos específicos en el directorio volumenes
kubectl apply -f volumenes/pv_blob_test.yaml
kubectl apply -f volumenes/pv_auth_test.yaml
kubectl apply -f volumenes/pvc_auth.yaml
kubectl apply -f volumenes/pvc__blob.yaml
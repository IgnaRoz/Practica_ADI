#!/bin/bash

# Eliminar todos los recursos en el namespace 'default'
kubectl delete --all all --namespace=default

# Eliminar todos los PersistentVolumeClaims (PVC)
kubectl delete pvc --all

# Eliminar todos los PersistentVolumes (PV)
kubectl delete pv --all

# Eliminar todos los Ingress
kubectl delete ingress --all

#Deistala controlado nginx para el ingress
#kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/cloud/deploy.yaml

#Desistala todos los servicio de ingress-nginx
#kubectl delete svc --all -n ingress-nginx

#!/bin/bash
sudo mv ./k3s /usr/local/bin/k3s
sudo chmod 644 /etc/rancher/k3s/k3s.yaml
sudo chown $(id -u):$(id -g) /etc/rancher/k3s/k3s.yaml
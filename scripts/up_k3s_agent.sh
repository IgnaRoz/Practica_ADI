#!/bin/bash
sudo ./k3s agent --server https://$1:6443 --token $2
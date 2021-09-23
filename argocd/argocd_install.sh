#!/bin/bash

# deploy ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# NodePort to access argocd ui
kubectl apply -f argocd-server-nodeport.yml

kubectl -n argocd get pod -w

# Installing the application
kubectl apply -f udaconnect-application.yml

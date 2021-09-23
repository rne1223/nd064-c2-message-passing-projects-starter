#!/bin/bash

ARGOCD_DIR="$HOME/udaconnect/argocd"
NAMESPACE='argocd'

# deploy ArgoCD
kubectl create namespace $NAMESPACE
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# NodePort to access argocd ui
kubectl apply -n $NAMESPACE -f "$ARGOCD_DIR/argocd-server-nodeport.yml"

kubectl -n argocd get pod -w

# Installing the application
kubectl apply -n $NAMESPACE -f "$ARGOCD_DIR/udaconnect-application.yml" 

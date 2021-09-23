#!/bin/bash

ARGOCD_DIR="$HOME/udaconnect/argocd"
ARGOCD_NAMESPACE='argocd'
APP_NAMESPACE='udaconnect'

# create namespaces
kubectl create namespace $ARGOCD_NAMESPACE
kubectl create namespace $APP_NAMESPACE


# deploy ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# NodePort to access argocd ui
kubectl apply -n $ARGOCD_NAMESPACE -f "$ARGOCD_DIR/argocd-server-nodeport.yml"

kubectl -n argocd get pod -w

# Installing the application
kubectl apply -n $ARGOCD_NAMESPACE -f "$ARGOCD_DIR/udaconnect-application.yml" 

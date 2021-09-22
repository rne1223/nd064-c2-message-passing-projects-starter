#!/bin/bash

NAME_SPACE="test"

kubectl create namespace $NAME_SPACE
kubectl apply -f ~/udaconnect/deployment -n $NAME_SPACE
helm install kafka bitnami/kafka -n $NAME_SPACE \
     --set volumePermissions.enabled=true \
     --set zookeeper.volumePermissions.enabled=true
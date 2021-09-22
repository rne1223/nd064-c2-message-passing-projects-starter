#!/bin/bash

NAME_SPACE="test"

# Simple script to get pod names
podName() { kubectl get pod -n $NAME_SPACE | grep $1 | awk '{ print $1 }'; }

kubectl create namespace $NAME_SPACE
kubectl apply -f ~/udaconnect/deployment -n $NAME_SPACE
helm install kafka bitnami/kafka -n $NAME_SPACE \
     --set volumePermissions.enabled=true \
     --set zookeeper.volumePermissions.enabled=true

kubectl get pods -n $NAME_SPACE -w

sh ~/udaconnect/scripts/run_db_command.sh $NAME_SPACE $(podName post) 
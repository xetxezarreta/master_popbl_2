#!/bin/bash

RED='\033[0;31m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'

if [ $1 == "dev" ] || [ $1 == "staging" ] || [ $1 == "prod" ] 
then
    ../k8s-configure.sh $1

    secret="$1-secret" 
    crt="../certs/$1.itapp.eus.crt"
    key="../certs/$1.itapp.eus.key"
    kubectl create secret tls $secret --cert $crt --key $key

    kubectl create secret docker-registry regcred --docker-server=registry.gitlab.com --docker-username=$2 --docker-password=$3 --docker-email=$4


    kubectl create -f k8s/persistent-volume/django.yaml
    kubectl create -f k8s/persistent-volume-claim/django.yaml
    kubectl create -f k8s/deployments/django-b.yaml
    kubectl create -f k8s/deployments/django-g.yaml
    kubectl create -f k8s/services/django.yaml
    kubectl create -f k8s/ingress/$1.yaml
else
    echo -en "${RED}"
    read -r "Error: specify [dev|staging|prod]"
    echo -en "${NC}" 
fi

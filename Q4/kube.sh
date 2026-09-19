#!/bin/bash
set -e

minikube image build -t spam-api:v1.0 .

kubectl apply -f deployment-service.yaml
kubectl rollout status deployment/spam-api-deployment

kubectl get pods -l app=spam-api -o wide

POD_TO_DELETE=$(kubectl get pods -l app=spam-api -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod "$POD_TO_DELETE"

sleep 4
kubectl get pods -l app=spam-api -o wide

sed -i 's/"version": "v1.0"/"version": "v2.0"/g' app.py

minikube image build -t spam-api:v2.0 .

kubectl set image deployment/spam-api-deployment spam-api=spam-api:v2.0
kubectl rollout status deployment/spam-api-deployment

kubectl rollout history deployment/spam-api-deployment
#!/bin/bash

kubectl apply -f k8/ns.yaml
kubectl apply -f k8/broker.yaml
kubectl apply -f k8/db.yaml
kubectl apply -f k8/all_us.yaml
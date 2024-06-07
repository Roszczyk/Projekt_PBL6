#!/bin/bash

kubectl apply -f k8s/ns.yml
kubectl apply -f k8s/broker.yml
kubectl apply -f k8s/db.yml
kubectl apply -f k8s/all_us.yml
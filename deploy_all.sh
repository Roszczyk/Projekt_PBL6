#!/bin/bash

kubectl apply -f k8/ns.yml
kubectl apply -f k8/broker.yml
kubectl apply -f k8/db.yml
kubectl apply -f k8/all_us.yml
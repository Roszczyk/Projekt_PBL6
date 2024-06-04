#!/bin/bash

kubectl get deployments -n pam-ns -o name | xargs -I {} kubectl rollout restart {} -n pam-ns
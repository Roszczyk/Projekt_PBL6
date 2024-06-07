kubectl create secret docker-registry docker-secret --docker-server=https://index.docker.io/v1/ --docker-username=piotrsicinski --docker-password=studentstudent --docker-email=piotr.sicinski.stud@pw.edu.pl

kubectl get secrets

kubectl describe secret docker-secret
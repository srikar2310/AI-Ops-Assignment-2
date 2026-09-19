python3 generate_shards.py
kubectl apply -f job-validator.yaml
kubectl get pods -l app=shard-validator -o wide
kubectl logs -l app=shard-validator --tail=-1
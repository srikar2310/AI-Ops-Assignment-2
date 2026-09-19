# Assignment 2: Docker & Kubernetes Ecosystem

This repository contains the implementation for Assignment 2, covering Docker optimization, Docker Compose networking with caching, Kubernetes batch processing (Indexed Jobs), and Kubernetes Deployments (Self-healing & Rolling Updates).

## Prerequisites
Ensure the following tools are installed on your system:
- **Docker & Docker Compose**
- **Minikube** (for multi-node local Kubernetes cluster)
- **kubectl** (Kubernetes command-line tool)
- **Python 3.10+**

---

## Question 1: Docker Image Optimization (Multi-stage Builds)
**Directory:** `Assign2/Q1`

This section demonstrates the reduction in Docker image size by migrating from a naive build approach to a multi-stage build pattern.

### Instructions:
1. Navigate to the Q1 directory:
   ```bash
   cd Assign2/Q1
   ```
2. Build the naive image:
   ```bash
   ./naive.sh
   ```
3. Build the optimized multi-stage image:
   ```bash
   ./mult.sh
   ```
4. Compare the image sizes output in your terminal to verify the multi-stage optimization.

---

## Question 2: Docker Compose & Redis Caching
**Directory:** `Assign2/Q2`

This section validates a multi-container environment where a FastAPI application utilizes a Redis caching layer to accelerate prediction latency.

### Instructions:
1. Navigate to the Q2 directory:
   ```bash
   cd Assign2/Q2
   ```
2. Launch the services in detached mode:
   ```bash
   docker compose up --build -d
   ```
3. Wait a few seconds for the API and Redis cache to initialize.
4. Run the benchmarking script to observe the speedup factor between a Cache MISS and a Cache HIT:
   ```bash
   python3 test_cache.py
   ```
5. Tear down the environment:
   ```bash
   docker compose down --volumes --remove-orphans
   ```

---

## Question 3: Kubernetes Indexed Jobs (Batch Processing)
**Directory:** `Assign2/Q3`

This section executes a batch processing job across a multi-node Kubernetes cluster. The job uses `parallelism: 4` to process 8 simulated CSV shards.

### Instructions:
1. Start a 2-node Minikube cluster:
   ```bash
   minikube start --nodes 2 --cpus 2 --memory 2048
   ```
2. Navigate to the Q3 directory:
   ```bash
   cd Assign2/Q3
   ```
3. Run the automated script which generates the synthetic shards, deploys the Indexed Job, and fetches the logs. 
   ```bash
   chmod +x kube.sh
   ./kube.sh
   ```
4. **Manual Verification (Optional):**
   - View parallel pod execution across nodes: `kubectl get pods -l app=shard-validator -o wide`
   - Fetch the validation reports: `kubectl logs -l app=shard-validator --tail=-1`

---

## Question 4: Kubernetes Deployments & Rolling Updates
**Directory:** `Assign2/Q4`

This section demonstrates managing long-running services in Kubernetes, showcasing self-healing capabilities and zero-downtime rolling updates on a multi-node cluster.

### Instructions:
1. Ensure your multi-node Minikube cluster from Q3 is still running.
2. Navigate to the Q4 directory:
   ```bash
   cd Assign2/Q4
   ```
3. Execute the automated workflow:
   ```bash
   chmod +x kube.sh
   ./kube.sh
   ```
4. **What the script does:**
   - Uses `minikube image build` to build the `v1.0` image synchronously across both cluster nodes.
   - Deploys the application and waits for the rollout to complete.
   - Simulates a node/pod failure by explicitly deleting an active pod, pausing to let you see the ReplicaSet immediately spawn a replacement.
   - Updates the source code to `v2.0` and triggers a rolling update.
   - Outputs the final rollout history.

## Cleanup
Once you have finished reviewing all components, safely tear down your local Kubernetes cluster:
```bash
minikube delete
```

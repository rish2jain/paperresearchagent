# 🎯 Next Steps After Nodegroup Creation

## ✅ Current Progress

**Nodegroup Creation:** ✅ **IN PROGRESS**
- **Name:** ng-gpu-nodes
- **Status:** CREATING
- **Capacity:** 2 nodes (min: 1, max: 3)
- **Instance Type:** g5.2xlarge (GPU)
- **ETA:** 5-10 minutes

---

## 📋 Once Nodegroup Completes

### Step 1: Verify Nodegroup is Ready

```bash
# Check nodegroup status
aws eks describe-nodegroup \
  --cluster-name research-ops-cluster \
  --nodegroup-name ng-gpu-nodes \
  --region us-east-2 \
  --query 'nodegroup.status'

# Should return: "ACTIVE"
```

### Step 2: Verify Nodes are Ready

```bash
# Update kubeconfig
aws eks update-kubeconfig --name research-ops-cluster --region us-east-2

# Check nodes
kubectl get nodes

# Should see 2 nodes in Ready state
# Example:
# NAME                                          STATUS   ROLES    AGE   VERSION
# ip-xxx-xxx-xxx-xxx.us-east-2.compute.internal   Ready    <none>   5m    v1.28.x
# ip-xxx-xxx-xxx-xxx.us-east-2.compute.internal   Ready    <none>   5m    v1.28.x
```

### Step 3: Continue with Deployment

Once nodes are ready, continue with the deployment:

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s

# Apply all Kubernetes manifests
kubectl apply -f namespace.yaml
kubectl apply -f secrets.yaml
kubectl apply -f reasoning-nim-deployment.yaml
kubectl apply -f embedding-nim-deployment.yaml
kubectl apply -f vector-db-deployment.yaml
kubectl apply -f agent-orchestrator-deployment.yaml
kubectl apply -f web-ui-deployment.yaml
kubectl apply -f ingress.yaml

# OR run the deploy script (it will detect existing cluster and skip cluster creation)
NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
export NGC_API_KEY
./deploy.sh
```

### Step 4: Verify Pods are Running

```bash
# Watch pod status
kubectl get pods -n research-ops -w

# Should see all pods in Running state:
# - reasoning-nim-xxx
# - embedding-nim-xxx
# - vector-db-xxx
# - agent-orchestrator-xxx
# - web-ui-xxx
```

### Step 5: Get Service Endpoints

```bash
# Get ingress URL
kubectl get ingress -n research-ops

# Get service URLs
kubectl get svc -n research-ops

# API endpoint will be available via ingress
```

### Step 6: Test the System

```bash
# Test health endpoint
curl http://<INGRESS_URL>/health

# Test research endpoint
curl -X POST http://<INGRESS_URL>/research/synthesize \
  -H "Content-Type: application/json" \
  -d '{"query": "quantum computing", "max_papers": 5}'
```

---

## ⏱️ Expected Timeline

- **Nodegroup Creation:** 5-10 minutes (current step)
- **Pod Deployment:** 5-10 minutes
- **Service Ready:** ~15 minutes total from now

---

## 🔍 Monitoring Commands

### Check Nodegroup Status:
```bash
aws eks describe-nodegroup \
  --cluster-name research-ops-cluster \
  --nodegroup-name ng-gpu-nodes \
  --region us-east-2 \
  --query 'nodegroup.status'
```

### Watch Pods:
```bash
kubectl get pods -n research-ops -w
```

### Check Logs:
```bash
# Agent orchestrator logs
kubectl logs -n research-ops -l app=agent-orchestrator --tail=50 -f

# Reasoning NIM logs
kubectl logs -n research-ops -l app=reasoning-nim --tail=50 -f

# Embedding NIM logs
kubectl logs -n research-ops -l app=embedding-nim --tail=50 -f
```

---

## 🚨 Troubleshooting

### If Nodegroup Stuck in CREATING:
```bash
# Check CloudFormation events for errors
aws cloudformation describe-stack-events \
  --region us-east-2 \
  --stack-name eksctl-research-ops-cluster-nodegroup-ng-gpu-nodes \
  --max-items 20 \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'
```

### If Nodes Not Joining:
```bash
# Check nodegroup status details
aws eks describe-nodegroup \
  --cluster-name research-ops-cluster \
  --nodegroup-name ng-gpu-nodes \
  --region us-east-2
```

---

## ✅ Success Criteria

1. ✅ Nodegroup status: ACTIVE
2. ✅ 2 nodes visible: `kubectl get nodes`
3. ✅ All pods running: `kubectl get pods -n research-ops`
4. ✅ Health endpoint responds: `/health`
5. ✅ Research endpoint works: `/research/synthesize`

---

**Current Status:** Nodegroup is CREATING. Wait 5-10 minutes, then proceed with Step 1 above.


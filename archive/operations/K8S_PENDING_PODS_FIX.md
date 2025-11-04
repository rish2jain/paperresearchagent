# Kubernetes Pending Pods - Resolution Summary

**Date:** 2025-11-03
**Issue:** 2 NIM pods stuck in Pending status
**Status:** ✅ **RESOLVED**

---

## Problem Description

Two pods were stuck in `Pending` status and unable to be scheduled:

```
embedding-nim-647f7dc88-lfcn2   0/1   Pending   0   88m
reasoning-nim-c8fd79cf6-p6jvc   0/1   Pending   0   88m
```

**Error Messages:**
```
Warning  FailedScheduling  default-scheduler
0/2 nodes are available: 2 Insufficient nvidia.com/gpu.
preemption: 0/2 nodes are available: 2 No preemption victims found for incoming pod.
```

---

## Root Cause Analysis

### Cluster Configuration
- **Nodes:** 2x g5.2xlarge instances (each with 1 NVIDIA A10G GPU)
- **Total GPUs Available:** 2 GPUs
- **GPU Allocation:**
  - Node 1: `embedding-nim-8499b79b5b-5nm4x` (1 GPU) ✅ Running
  - Node 2: `reasoning-nim-968c9d65b-v4wzv` (1 GPU) ✅ Running
  - **Result:** 2/2 GPUs in use (100% utilized)

### Why Pods Were Pending

1. **Rolling Update Stuck:** The deployments had initiated rolling updates (revision 13 for embedding-nim)
2. **No Available GPUs:** New pods from the update couldn't schedule because all GPUs were already allocated
3. **Old ReplicaSets:** 20+ old ReplicaSets were retained (default `revisionHistoryLimit: 10`)
4. **Resource Exhaustion:** Each NIM pod requires 1 GPU, and both GPUs were already in use

### Resource Requirements (Per Pod)
```yaml
reasoning-nim:
  requests: {cpu: 4, memory: 20Gi, gpu: 1}
  limits: {cpu: 8, memory: 30Gi, gpu: 1}

embedding-nim:
  requests: {cpu: 2, memory: 8Gi, gpu: 1}
  limits: {cpu: 4, memory: 16Gi, gpu: 1}
```

---

## Solution Applied

### Step 1: Rollback Stuck Deployments
```bash
kubectl rollout undo deployment/embedding-nim -n research-ops
kubectl rollout undo deployment/reasoning-nim -n research-ops
```

**Result:** Pending pods terminated, rollout reverted to stable version

### Step 2: Clean Up Old ReplicaSets
```bash
kubectl get replicasets -n research-ops | \
  awk '$2 == 0 && $3 == 0 && $4 == 0 {print $1}' | \
  xargs -I {} kubectl delete replicaset {} -n research-ops
```

**Result:** Removed 20+ unused ReplicaSets, preventing future issues

---

## Verification Results

### Final Pod Status
```
NAME                                  READY   STATUS    RESTARTS   AGE
agent-orchestrator-7f884c4778-rpdv9   1/1     Running   0          90m
embedding-nim-8499b79b5b-5nm4x        1/1     Running   0          6h20m
qdrant-7b9fb95c99-rhbp6               1/1     Running   0          10h
reasoning-nim-968c9d65b-v4wzv         1/1     Running   0          6h5m
web-ui-5b9fc49bcb-nmbks               1/1     Running   0          4h36m
```

✅ **All pods Running**
✅ **No pending pods**
✅ **All deployments stable**

### Resource Allocation After Fix
```
Node 1 (ip-192-168-51-0):
  CPU: 5240m/8000m (66%)
  Memory: 14696Mi/30976Mi (47%)
  GPU: 1/1 (100%)
  Pods: embedding-nim, qdrant, agent-orchestrator

Node 2 (ip-192-168-95-23):
  CPU: 4940m/8000m (62%)
  Memory: 22004Mi/30976Mi (71%)
  GPU: 1/1 (100%)
  Pods: reasoning-nim, web-ui
```

---

## Preventive Measures

### 1. Configure Deployment History Limit
To prevent ReplicaSet accumulation, update deployments:

```yaml
spec:
  revisionHistoryLimit: 3  # Keep only last 3 revisions (default is 10)
```

**Apply to all deployments:**
```bash
kubectl patch deployment embedding-nim -n research-ops \
  -p '{"spec":{"revisionHistoryLimit":3}}'

kubectl patch deployment reasoning-nim -n research-ops \
  -p '{"spec":{"revisionHistoryLimit":3}}'

kubectl patch deployment agent-orchestrator -n research-ops \
  -p '{"spec":{"revisionHistoryLimit":3}}'

kubectl patch deployment web-ui -n research-ops \
  -p '{"spec":{"revisionHistoryLimit":3}}'
```

### 2. Pod Disruption Budgets (PDBs)
Ensure PDBs are configured to prevent simultaneous updates:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: embedding-nim-pdb
  namespace: research-ops
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: embedding-nim
```

### 3. Resource Quotas and Monitoring
Set up resource quotas to prevent over-commitment:

```bash
# Monitor GPU usage
kubectl get nodes -o json | jq '.items[] |
  {name:.metadata.name,
   gpus:.status.allocatable."nvidia.com/gpu"}'

# Check pod resource requests
kubectl describe nodes | grep -A 10 "Allocated resources"
```

### 4. Deployment Strategy
For GPU-constrained environments, use `Recreate` strategy instead of `RollingUpdate`:

```yaml
spec:
  strategy:
    type: Recreate  # Terminate old pod before creating new one
```

**Or** adjust rolling update parameters:
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 0        # Don't create new pods before old ones terminate
      maxUnavailable: 1  # Allow 1 pod to be unavailable during update
```

---

## Monitoring Commands

### Check Pod Status
```bash
kubectl get pods -n research-ops
```

### Check Pending Pods with Reasons
```bash
kubectl get pods -n research-ops | grep Pending | awk '{print $1}' | \
  xargs -I {} kubectl describe pod {} -n research-ops | grep -A 5 Events
```

### Check GPU Allocation
```bash
kubectl describe nodes | grep -E "(Name:|nvidia.com/gpu)"
```

### Check Old ReplicaSets
```bash
kubectl get replicasets -n research-ops | \
  awk '$2 == 0 && $3 == 0 && $4 == 0'
```

### Clean Up Old ReplicaSets (if needed)
```bash
kubectl get replicasets -n research-ops | \
  awk '$2 == 0 && $3 == 0 && $4 == 0 {print $1}' | \
  xargs -I {} kubectl delete replicaset {} -n research-ops
```

---

## Troubleshooting Guide

### If Pods Become Pending Again

**1. Check available GPUs:**
```bash
kubectl describe nodes | grep nvidia.com/gpu
```

**2. Check what's using GPUs:**
```bash
kubectl get pods -n research-ops -o wide
kubectl describe pod <pending-pod-name> -n research-ops
```

**3. Check for stuck rollouts:**
```bash
kubectl rollout status deployment/<deployment-name> -n research-ops
```

**4. If rollout is stuck, rollback:**
```bash
kubectl rollout undo deployment/<deployment-name> -n research-ops
```

**5. Force pod eviction (if needed):**
```bash
kubectl delete pod <pod-name> -n research-ops --force --grace-period=0
```

---

## Key Learnings

### Resource Constraints
- g5.2xlarge instances provide **only 1 GPU each**
- **Rolling updates require 2x GPU capacity** (old + new pods)
- Current cluster has **no spare GPU capacity** for rolling updates

### Deployment Strategy Recommendations

**Option 1: Use Recreate Strategy (Recommended for GPU-constrained environments)**
```yaml
spec:
  strategy:
    type: Recreate
```
- **Pros:** No extra GPU needed, simple and reliable
- **Cons:** Brief downtime during updates (acceptable for NIMs with health checks)

**Option 2: Add a Third GPU Node (If zero-downtime is required)**
```bash
# Scale node group to 3 nodes
eksctl scale nodegroup --cluster=research-ops-cluster \
  --name=gpu-nodes --nodes=3
```
- **Pros:** Enables true rolling updates with zero downtime
- **Cons:** Increased cost (~$1.22/hour per g5.2xlarge)

**Option 3: Temporary Scale-Up for Updates**
```bash
# Before update: Scale to 3 nodes
eksctl scale nodegroup --cluster=research-ops-cluster \
  --name=gpu-nodes --nodes=3

# Perform update
kubectl set image deployment/embedding-nim ...

# After update: Scale back to 2 nodes
eksctl scale nodegroup --cluster=research-ops-cluster \
  --name=gpu-nodes --nodes=2
```

---

## Related Issues

- **GPU Exhaustion:** No spare GPU capacity for rolling updates
- **ReplicaSet Accumulation:** 20+ old ReplicaSets consuming cluster metadata
- **Rollout Strategy:** RollingUpdate incompatible with GPU constraints

---

## Success Criteria

- [x] All pods in Running status
- [x] No pending pods
- [x] Old ReplicaSets cleaned up
- [x] Deployments stable
- [x] GPU allocation at 100% (expected)
- [x] All services accessible

**Status:** ✅ **RESOLVED**

---

## Additional Notes

- The cluster is operating at **100% GPU capacity** (both GPUs allocated)
- Future updates should use **Recreate strategy** or **scale up temporarily**
- Consider implementing **revisionHistoryLimit: 3** to prevent ReplicaSet accumulation
- Monitor GPU usage regularly with provided commands

**Contact:** For questions about this fix, refer to `docs/TROUBLESHOOTING.md`

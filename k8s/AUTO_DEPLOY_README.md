# 🤖 Automated Deployment Script

## Overview

The `auto_deploy_wait_quota.sh` script automatically:
1. ✅ Monitors AWS quota approval status (checks every 5 minutes)
2. ✅ Creates nodegroup when quota is approved
3. ✅ Verifies nodegroup is ready
4. ✅ Deploys all Kubernetes services
5. ✅ Waits for pods to be ready

## Usage

### Start Automated Deployment

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s
./auto_deploy_wait_quota.sh
```

### What It Does

1. **Monitor Quota** (Step 1)
   - Checks On-Demand G instance quota status every 5 minutes
   - Maximum wait: 6 hours
   - Exits when quota is APPROVED or DENIED

2. **Create Nodegroup** (Step 2)
   - Creates `ng-gpu-nodes` with 2x g5.2xlarge instances
   - Takes 10-15 minutes

3. **Verify Nodegroup** (Step 3)
   - Waits for nodegroup to be ACTIVE
   - Verifies nodes are visible in cluster
   - Maximum wait: 15 minutes (30 checks × 30 seconds)

4. **Deploy Services** (Step 4)
   - Applies all Kubernetes manifests
   - Waits for pods to be ready
   - Shows service endpoints and test commands

## Monitoring Quota Manually

If you want to check quota status without running the full script:

```bash
./check_quota_status.sh
```

## Expected Timeline

- **Quota Approval:** 1-4 hours (usually 1-2 hours)
- **Nodegroup Creation:** 10-15 minutes
- **Pod Deployment:** 5-10 minutes
- **Total:** ~2-5 hours (mostly waiting for quota)

## Running in Background

To run in background and save output:

```bash
nohup ./auto_deploy_wait_quota.sh > deployment.log 2>&1 &
tail -f deployment.log
```

## Stopping the Script

If you need to stop the script:

```bash
# Find the process
ps aux | grep auto_deploy_wait_quota

# Kill it
kill <PID>
```

## Troubleshooting

### Quota Not Approved After 6 Hours

1. Check status manually:
   ```bash
   ./check_quota_status.sh
   ```

2. Check AWS Console:
   - Go to: https://console.aws.amazon.com/servicequotas/home?region=us-east-2
   - Search for: "Running On-Demand G and VT instances"
   - Check request status

3. Contact AWS Support if needed

### Nodegroup Creation Fails

Check the error message. Common issues:
- Quota still insufficient (check actual quota value)
- Region-specific issues
- Instance availability

### Pods Not Starting

Check pod status:
```bash
kubectl get pods -n research-ops
kubectl describe pod <pod-name> -n research-ops
kubectl logs <pod-name> -n research-ops
```

## Manual Steps (If Script Fails)

If the script fails at any step, you can continue manually:

### After Quota Approval:

```bash
eksctl create nodegroup \
  --cluster research-ops-cluster \
  --region us-east-2 \
  --name ng-gpu-nodes \
  --node-type g5.2xlarge \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

### After Nodegroup Created:

```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s
export NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
aws eks update-kubeconfig --name research-ops-cluster --region us-east-2
kubectl apply -f namespace.yaml
kubectl apply -f secrets.yaml
kubectl apply -f reasoning-nim-deployment.yaml
kubectl apply -f embedding-nim-deployment.yaml
kubectl apply -f vector-db-deployment.yaml
kubectl apply -f agent-orchestrator-deployment.yaml
kubectl apply -f web-ui-deployment.yaml
kubectl apply -f ingress.yaml
```

## Script Configuration

You can modify these variables in the script:

```bash
REGION="us-east-2"                    # AWS region
CLUSTER_NAME="research-ops-cluster"   # EKS cluster name
NODEGROUP_NAME="ng-gpu-nodes"         # Nodegroup name
CHECK_INTERVAL=300                    # Check every 5 minutes
MAX_WAIT_HOURS=6                      # Maximum wait time
```

## Log Files

If running with `nohup`, check:
- `deployment.log` - Full script output
- `nohup.out` - Alternative log location

## Success Criteria

The script is successful when:
1. ✅ Quota status = APPROVED
2. ✅ Nodegroup status = ACTIVE
3. ✅ Nodes visible: `kubectl get nodes`
4. ✅ All pods running: `kubectl get pods -n research-ops`
5. ✅ Health endpoint responds: `curl http://<ingress>/health`

---

**Next Step:** Run `./auto_deploy_wait_quota.sh` and let it handle everything!


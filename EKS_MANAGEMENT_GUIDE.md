# EKS Resource Management Guide

Complete guide for managing your ResearchOps Agent deployment on AWS EKS with proper lifecycle controls, cost optimization, and recreation strategies.

---

## 🎯 Quick Reference

```bash
# Make script executable
chmod +x manage-eks.py

# Check deployment status
./manage-eks.py status --detailed

# View logs
./manage-eks.py logs agent-orchestrator --follow

# Restart a service
./manage-eks.py restart reasoning-nim

# Cost estimation
./manage-eks.py cost

# Health check
./manage-eks.py health

# Cleanup namespace
./manage-eks.py cleanup --level namespace

# Delete entire cluster
./manage-eks.py cleanup --level cluster
```

---

## 📊 Resource Management

### Check Status

**Quick status:**
```bash
./manage-eks.py status
```

**Detailed status with resource usage:**
```bash
./manage-eks.py status --detailed
```

**Output includes:**
- Pod status (Running, Pending, etc.)
- Service endpoints (LoadBalancer IPs)
- Resource usage (CPU, memory)
- Restart counts

### Monitor Logs

**View recent logs:**
```bash
./manage-eks.py logs agent-orchestrator
./manage-eks.py logs reasoning-nim --tail 200
```

**Follow logs in real-time:**
```bash
./manage-eks.py logs web-ui --follow
```

**Available deployments:**
- `reasoning-nim`
- `embedding-nim`
- `qdrant` (vector database)
- `agent-orchestrator`
- `web-ui`

### Health Checks

**Comprehensive health check:**
```bash
./manage-eks.py health
```

**Checks:**
- ✅ All pods running
- ✅ Services have external IPs (if LoadBalancer)
- ✅ No excessive restarts
- ✅ Exit code 0 if healthy, 1 if issues found

---

## 🔄 Updates and Rollbacks

### Apply Updates

**Update all deployments:**
```bash
./manage-eks.py update
```

**What it does:**
1. Applies latest Kubernetes manifests from `k8s/` directory
2. Triggers rolling updates for changed deployments
3. Preserves existing resources

**After updating code:**
```bash
# 1. Build new images
docker build -f Dockerfile.orchestrator -t myregistry.io/orchestrator:v2 .
docker push myregistry.io/orchestrator:v2

# 2. Update image in k8s/agent-orchestrator-deployment.yaml

# 3. Apply update
./manage-eks.py update

# 4. Monitor rollout
kubectl rollout status deployment/agent-orchestrator -n research-ops
```

### Restart Deployments

**Restart without downtime (rolling restart):**
```bash
./manage-eks.py restart agent-orchestrator
./manage-eks.py restart reasoning-nim
```

**When to restart:**
- After configuration changes
- To refresh connections
- To clear memory leaks
- After secret updates

### Rollback

**Rollback to previous version:**
```bash
./manage-eks.py rollback agent-orchestrator
```

**Rollback to specific revision:**
```bash
# View revision history first
kubectl rollout history deployment/agent-orchestrator -n research-ops

# Rollback to specific revision
kubectl rollout undo deployment/agent-orchestrator --to-revision=2 -n research-ops
```

---

## 🔧 Scaling

### Manual Scaling

**Scale web-ui for load:**
```bash
./manage-eks.py scale web-ui --replicas 3
```

**Scale down to save costs:**
```bash
./manage-eks.py scale agent-orchestrator --replicas 1
```

### Auto-Scaling (HPA)

**Enable horizontal pod autoscaler:**
```bash
# Already configured in k8s/hpa-agent-orchestrator.yaml
kubectl apply -f k8s/hpa-agent-orchestrator.yaml

# View HPA status
kubectl get hpa -n research-ops

# Check scaling events
kubectl describe hpa agent-orchestrator-hpa -n research-ops
```

**HPA Configuration:**
- Min replicas: 1
- Max replicas: 5
- Target CPU: 70%
- Scale up: when CPU > 70% for 30s
- Scale down: when CPU < 70% for 5 min

---

## 🗑️ Cleanup and Recreation

### Cleanup Levels

**1. Pod cleanup (no downtime):**
```bash
./manage-eks.py cleanup --level pods
```
- Deletes all pods
- Deployments recreate them automatically
- Use for stuck pods

**2. Namespace cleanup (removes all resources):**
```bash
./manage-eks.py cleanup --level namespace
```
- Deletes entire namespace and all resources
- Cluster remains intact
- Re-deploy with `./quick-deploy.sh`
- **Downtime:** Complete

**3. Cluster cleanup (removes everything):**
```bash
./manage-eks.py cleanup --level cluster
```
- Deletes entire EKS cluster
- Requires cluster name confirmation
- **Savings:** ~$2/hour (~$1,500/month)
- **Downtime:** Complete

### Recreation Workflows

**Recreate specific components:**
```bash
# Recreate reasoning NIM (e.g., to use new image)
./manage-eks.py recreate --components reasoning-nim

# Recreate multiple components
./manage-eks.py recreate --components reasoning-nim embedding-nim
```

**What happens:**
1. Deletes deployment
2. Waits 5 seconds for cleanup
3. Applies manifest from `k8s/` directory
4. New pods start with fresh state

**Use cases:**
- Update to new NIM version
- Clear persistent state
- Fix configuration issues
- Force image pull

**Full recreation workflow:**
```bash
# 1. Backup current state
./manage-eks.py backup --output-dir ./backups

# 2. Delete namespace
./manage-eks.py cleanup --level namespace

# 3. Wait for deletion
kubectl get namespaces -w

# 4. Redeploy
./quick-deploy.sh

# 5. Verify
./manage-eks.py health
```

---

## 💰 Cost Management

### Cost Estimation

**Current cost estimate:**
```bash
./manage-eks.py cost
```

**Output:**
```
💰 Cost Estimation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Cluster Resources:
  Nodes: 2

💵 Estimated Costs (assuming g5.2xlarge nodes):
  Hourly:  $2.11
  Daily:   $50.64
  Monthly: $1,519.20

💡 Cost Optimization Tips:
  • Scale down to 1 node when not in use: Save $1.01/hour
  • Delete cluster when not needed: Save $2.11/hour
  • Use Spot instances: Save up to 70%
```

### Cost Optimization Strategies

**1. Scale Down During Idle Periods**
```bash
# Before leaving for the day
./manage-eks.py scale agent-orchestrator --replicas 0
./manage-eks.py scale web-ui --replicas 0

# NIMs can't scale to 0, so delete if not needed
kubectl delete deployment reasoning-nim -n research-ops
kubectl delete deployment embedding-nim -n research-ops

# Next day, redeploy
kubectl apply -f k8s/reasoning-nim-deployment.yaml
kubectl apply -f k8s/embedding-nim-deployment.yaml
```

**2. Delete Cluster When Not Needed**
```bash
# Backup before deletion
./manage-eks.py backup

# Delete cluster
./manage-eks.py cleanup --level cluster

# When needed again
./quick-deploy.sh
```

**3. Use Spot Instances**

Edit `k8s/cluster-config-spot.yaml`:
```yaml
managedNodeGroups:
  - name: spot-nodes
    instanceTypes: ["g5.2xlarge"]
    spot: true
    minSize: 1
    maxSize: 3
    desiredCapacity: 2
```

Create with spot instances:
```bash
eksctl create cluster -f k8s/cluster-config-spot.yaml
```

**Savings:** Up to 70% off on-demand pricing

**4. Right-Size Resources**

```bash
# Check actual usage
kubectl top pods -n research-ops

# Adjust resource requests in manifests
# Edit k8s/*-deployment.yaml
# Reduce CPU/memory requests if overprovisioned
```

---

## 💾 Backup and Restore

### Create Backup

**Manual backup:**
```bash
./manage-eks.py backup --output-dir ./backups
```

**What's backed up:**
- Deployments
- Services
- ConfigMaps
- Secrets
- Pod configurations

**Backup location:**
```
./backups/backup-20250115-143022/
├── deployments.yaml
├── services.yaml
├── configmaps.yaml
├── secrets.yaml
└── pods.yaml
```

### Restore from Backup

**Restore all resources:**
```bash
cd backups/backup-20250115-143022

# Apply all resources
kubectl apply -f deployments.yaml
kubectl apply -f services.yaml
kubectl apply -f configmaps.yaml
kubectl apply -f secrets.yaml
```

**Selective restore:**
```bash
# Restore only specific deployment
kubectl apply -f deployments.yaml --selector=app=agent-orchestrator
```

---

## 🔄 Common Workflows

### Daily Operations

**Morning startup:**
```bash
# 1. Check status
./manage-eks.py status

# 2. Health check
./manage-eks.py health

# 3. View recent logs
./manage-eks.py logs agent-orchestrator --tail 50
```

**End of day:**
```bash
# 1. Backup state
./manage-eks.py backup

# 2. Scale down (optional)
./manage-eks.py scale agent-orchestrator --replicas 0
./manage-eks.py scale web-ui --replicas 0

# 3. Check cost estimate
./manage-eks.py cost
```

### Troubleshooting Workflow

**Service not responding:**
```bash
# 1. Check pod status
./manage-eks.py status --detailed

# 2. View logs
./manage-eks.py logs <deployment> --tail 200

# 3. Check events
kubectl get events -n research-ops --sort-by='.lastTimestamp'

# 4. Restart if needed
./manage-eks.py restart <deployment>

# 5. If still failing, recreate
./manage-eks.py recreate --components <deployment>
```

### Update Workflow

**Deploying new code:**
```bash
# 1. Backup current state
./manage-eks.py backup

# 2. Build and push new images
docker build -t myregistry.io/orchestrator:v2 .
docker push myregistry.io/orchestrator:v2

# 3. Update manifest
# Edit k8s/agent-orchestrator-deployment.yaml
# Change image tag to :v2

# 4. Apply update
./manage-eks.py update

# 5. Monitor rollout
kubectl rollout status deployment/agent-orchestrator -n research-ops

# 6. Verify
./manage-eks.py health

# 7. If issues, rollback
./manage-eks.py rollback agent-orchestrator
```

### Cost Optimization Workflow

**Weekly cost review:**
```bash
# 1. Check current costs
./manage-eks.py cost

# 2. Review resource usage
kubectl top nodes
kubectl top pods -n research-ops

# 3. Identify idle periods
# (Check CloudWatch metrics)

# 4. Plan scaling schedule
# (Use cron to scale down during nights/weekends)

# 5. Consider spot instances
# (If availability requirements allow)
```

---

## 📈 Monitoring and Alerts

### CloudWatch Integration

**View EKS metrics in AWS Console:**
```
CloudWatch → Container Insights → research-ops-cluster
```

**Metrics to monitor:**
- Pod CPU utilization
- Pod memory utilization
- Node CPU/memory
- Network throughput
- GPU utilization

### Set Up Alerts

**CloudWatch Alarms:**
```bash
# Example: Alert on high pod CPU
aws cloudwatch put-metric-alarm \
  --alarm-name research-ops-high-cpu \
  --alarm-description "Alert when pod CPU > 80%" \
  --metric-name pod_cpu_utilization \
  --namespace ContainerInsights \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

### Custom Metrics

**Application metrics:**
```python
# In your code (using prometheus-client)
from prometheus_client import Counter, Histogram

request_count = Counter('research_requests_total', 'Total research requests')
request_duration = Histogram('research_duration_seconds', 'Research duration')
```

---

## 🚨 Emergency Procedures

### Cluster Unresponsive

```bash
# 1. Check AWS console for cluster health
# AWS Console → EKS → research-ops-cluster

# 2. Try updating kubeconfig
aws eks update-kubeconfig --name research-ops-cluster --region us-east-2

# 3. Check nodes
kubectl get nodes

# 4. If nodes down, check ASG in EC2 console
# EC2 → Auto Scaling Groups

# 5. Nuclear option: recreate cluster
./manage-eks.py cleanup --level cluster
./quick-deploy.sh
```

### NIMs Not Starting

```bash
# 1. Check events
kubectl describe pod <reasoning-nim-pod> -n research-ops

# 2. Common issues:
#    - NGC_API_KEY invalid
#    - GPU not available
#    - Image pull failure

# 3. Fix and recreate
./manage-eks.py recreate --components reasoning-nim
```

### Out of Memory

```bash
# 1. Identify memory-hungry pods
kubectl top pods -n research-ops --sort-by=memory

# 2. Increase memory limits
# Edit k8s/*-deployment.yaml
# Increase resources.limits.memory

# 3. Apply update
./manage-eks.py update

# 4. Or add more nodes
# Edit node count in cluster config
```

---

## 📚 Best Practices

### DO

✅ **Backup before major changes**
```bash
./manage-eks.py backup
```

✅ **Monitor costs regularly**
```bash
./manage-eks.py cost
```

✅ **Use rolling updates**
```bash
./manage-eks.py update  # Not delete + recreate
```

✅ **Test in namespace first**
```bash
# Create test namespace
kubectl create namespace research-ops-test
# Deploy there first
```

✅ **Keep backups**
```bash
# Automated backup script
./manage-eks.py backup --output-dir ./backups/$(date +%Y%m%d)
```

### DON'T

❌ **Don't delete cluster without backup**
❌ **Don't scale NIMs to 0 (doesn't work well)**
❌ **Don't force-delete pods unless necessary**
❌ **Don't ignore health check warnings**
❌ **Don't leave cluster running 24/7 if not needed**

---

## 🔧 Automation Scripts

### Daily Health Check Cron

```bash
# Add to crontab: crontab -e
0 9 * * * cd /path/to/research-ops-agent && ./manage-eks.py health || mail -s "Health Check Failed" your@email.com
```

### Auto-Scale Down Nights

```bash
# Scale down at 6 PM
0 18 * * * cd /path/to/research-ops-agent && ./manage-eks.py scale agent-orchestrator --replicas 0

# Scale up at 8 AM
0 8 * * * cd /path/to/research-ops-agent && ./manage-eks.py scale agent-orchestrator --replicas 2
```

### Weekly Backup

```bash
# Every Sunday at 2 AM
0 2 * * 0 cd /path/to/research-ops-agent && ./manage-eks.py backup --output-dir ./backups/$(date +%Y%m%d)
```

---

## 📊 Dashboard

### Create Monitoring Dashboard

```bash
# Install Kubernetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Create admin user
kubectl create serviceaccount dashboard-admin -n kubernetes-dashboard
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:dashboard-admin

# Get token
kubectl create token dashboard-admin -n kubernetes-dashboard

# Access dashboard
kubectl proxy
# Visit: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

---

## Summary

Key management commands:

| Task | Command |
|------|---------|
| Check status | `./manage-eks.py status --detailed` |
| View logs | `./manage-eks.py logs <deployment> --follow` |
| Restart service | `./manage-eks.py restart <deployment>` |
| Scale | `./manage-eks.py scale <deployment> --replicas N` |
| Update | `./manage-eks.py update` |
| Rollback | `./manage-eks.py rollback <deployment>` |
| Recreate | `./manage-eks.py recreate --components <deployment>` |
| Health check | `./manage-eks.py health` |
| Cost estimate | `./manage-eks.py cost` |
| Backup | `./manage-eks.py backup` |
| Cleanup namespace | `./manage-eks.py cleanup --level namespace` |
| Delete cluster | `./manage-eks.py cleanup --level cluster` |

**Save costs:** Delete cluster when not in use (~$2/hour savings)
**Best practice:** Backup before major changes
**Monitoring:** Run health checks daily

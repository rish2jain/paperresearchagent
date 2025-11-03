# 🚨 EKS Deployment Troubleshooting

## Issue: Elastic IP Limit Reached

**Error Message:**
```
The maximum number of addresses has been reached.
(Service: Ec2, Status Code: 400)
```

**Cause:** AWS account has reached the default limit of 5 Elastic IPs per region.

---

## 🔧 Solution Options

### Option 1: Release Unused Elastic IPs (Recommended)

#### Step 1: List All Elastic IPs
```bash
aws ec2 describe-addresses --region us-east-1 \
  --query 'Addresses[].{AllocationId:AllocationId,PublicIp:PublicIp,AssociationId:AssociationId}' \
  --output table
```

#### Step 2: Identify Unassociated Elastic IPs
Look for addresses where `AssociationId` is `null` or empty - these are unused.

#### Step 3: Release Unused Elastic IPs
```bash
# Replace ALLOCATION_ID with the actual allocation ID from Step 1
aws ec2 release-address --allocation-id eipalloc-xxxxxxxxx --region us-east-1
```

**⚠️ Warning:** Only release IPs that are truly unused. Don't release IPs associated with running resources.

#### Step 4: Retry Deployment
```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s
NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
export NGC_API_KEY
./deploy.sh
```

---

### Option 2: Request Elastic IP Limit Increase

#### Step 1: Request Quota Increase
1. Go to: https://console.aws.amazon.com/servicequotas/
2. Search for "EC2"
3. Find "EC2-VPC Elastic IPs"
4. Click "Request quota increase"
5. Enter new limit (e.g., 10 or 15)
6. Submit request

**Note:** Approval can take 24-48 hours, but often happens faster.

#### Step 2: Retry Deployment After Approval
Once approved, retry the deployment.

---

### Option 3: Use Different Region (Quick Workaround)

#### Step 1: Choose Alternative Region
Good alternatives:
- `us-east-2` (Ohio)
- `us-west-2` (Oregon)
- `eu-west-1` (Ireland)

#### Step 2: Update Deployment Script
```bash
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s

# Edit deploy.sh
# Change --region us-east-1 to --region us-east-2 (or another region)

# Also update secrets.yaml:
# Change AWS_DEFAULT_REGION: "us-east-1" to "us-east-2"
```

#### Step 3: Retry Deployment
```bash
NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
export NGC_API_KEY
./deploy.sh
```

---

### Option 4: Clean Up Failed Cluster First

#### Step 1: Check for Partial Resources
```bash
# Check if any resources were created
aws eks describe-cluster --name research-ops-cluster --region us-east-1 2>&1
aws cloudformation describe-stacks --region us-east-1 | grep research-ops
```

#### Step 2: Clean Up Failed Cluster
```bash
# This will clean up any partial resources
eksctl delete cluster --name research-ops-cluster --region us-east-1

# Or manually delete CloudFormation stacks
aws cloudformation delete-stack --stack-name eksctl-research-ops-cluster-cluster --region us-east-1
```

#### Step 3: Retry After Cleanup
After cleanup completes, retry deployment.

---

## 🔍 Quick Diagnostic Commands

### Check Elastic IP Usage
```bash
# Count total Elastic IPs
aws ec2 describe-addresses --region us-east-1 --query 'length(Addresses)'

# List all Elastic IPs with details
aws ec2 describe-addresses --region us-east-1 \
  --query 'Addresses[].{AllocId:AllocationId,IP:PublicIp,Assoc:AssociationId,Instance:InstanceId}' \
  --output table

# Find unassociated (unused) Elastic IPs
aws ec2 describe-addresses --region us-east-1 \
  --filters "Name=domain,Values=vpc" \
  --query 'Addresses[?AssociationId==null].{AllocId:AllocationId,IP:PublicIp}' \
  --output table
```

### Check Current Quota
```bash
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-0263D0A3 \
  --region us-east-1 \
  --query 'Quota.{Value:Value,Unit:Unit}' \
  --output table
```

### Check Existing Clusters
```bash
# List all EKS clusters
aws eks list-clusters --region us-east-1

# Check specific cluster
aws eks describe-cluster --name research-ops-cluster --region us-east-1 2>&1
```

---

## ✅ Recommended Action Plan

### Immediate Steps:

1. **Check Elastic IP Usage**
   ```bash
   aws ec2 describe-addresses --region us-east-1 \
     --query 'Addresses[?AssociationId==null].{AllocId:AllocationId,IP:PublicIp}' \
     --output table
   ```

2. **Release Unused Elastic IPs** (if any found)
   ```bash
   # For each unused Elastic IP:
   aws ec2 release-address --allocation-id eipalloc-xxxxxxxxx --region us-east-1
   ```

3. **Retry Deployment**
   ```bash
   cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s
   NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
   export NGC_API_KEY
   ./deploy.sh
   ```

### If No Unused Elastic IPs Available:

1. **Request Quota Increase** (Option 2 above)
2. **OR Use Different Region** (Option 3 above) - **Faster option**

---

## 🎯 Quick Fix: Use Different Region

The fastest solution if you can't release Elastic IPs:

```bash
# 1. Update secrets.yaml to use different region
nano k8s/secrets.yaml
# Change: AWS_DEFAULT_REGION: "us-east-1" to "us-east-2"

# 2. Update deploy.sh to use different region
nano k8s/deploy.sh
# Change all occurrences of --region us-east-1 to --region us-east-2

# 3. Retry deployment
cd k8s
NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
export NGC_API_KEY
./deploy.sh
```

---

## 📊 Alternative: Use Existing Cluster

If you have an existing EKS cluster:

1. **Use Existing Cluster**
   ```bash
   # Get existing cluster name
   aws eks list-clusters --region us-east-1

   # Update kubeconfig
   aws eks update-kubeconfig --name YOUR_EXISTING_CLUSTER --region us-east-1

   # Deploy services manually (skip cluster creation)
   cd k8s
   kubectl apply -f namespace.yaml
   kubectl apply -f secrets.yaml
   kubectl apply -f reasoning-nim-deployment.yaml
   # ... etc
   ```

2. **Verify Cluster Has GPU Nodes**
   ```bash
   # Check node types
   kubectl get nodes -o wide

   # Ensure GPU nodes available
   kubectl describe nodes | grep "nvidia.com/gpu"
   ```

---

## 💡 Prevention Tips

1. **Clean up unused resources regularly**
   - Release unused Elastic IPs
   - Delete unused EIPs from previous deployments

2. **Request quota increase proactively**
   - Increase Elastic IP limit to 10-15 for development

3. **Use different regions**
   - Spread resources across regions
   - Reduces dependency on single region limits

---

## 🆘 Still Stuck?

1. **Check AWS Support Console**
   - Request Elastic IP quota increase (can approve quickly)

2. **Try Different Region**
   - us-east-2, us-west-2, eu-west-1
   - No quota increase needed

3. **Manual Deployment**
   - Create cluster with eksctl manually
   - Deploy services step-by-step

---

**Next Step:** Choose one of the solution options above and retry deployment.


# 🚨 AWS Quota Issues - Summary

## ❌ Both Attempts Failed

### Attempt 1: On-Demand Instances (g5.2xlarge)
**Error:** `VcpuLimitExceeded`
- **Issue:** vCPU limit of 0 for g5.2xlarge instances
- **Reason:** AWS account has no quota allocated for GPU instances
- **Status:** ROLLBACK_COMPLETE

### Attempt 2: Spot Instances (g5.2xlarge)
**Error:** `MaxSpotInstanceCountExceeded`
- **Issue:** Maximum spot instance count exceeded
- **Reason:** Account has reached or exceeded spot instance limit for g5.2xlarge
- **Status:** ROLLBACK_COMPLETE

---

## 🔍 Root Cause Analysis

Your AWS account has **restricted quotas** for GPU instances:

1. **On-Demand vCPU Limit:** 0 for G-family instances
2. **Spot Instance Limit:** Exceeded or set to 0 for g5.2xlarge

This is common for:
- New AWS accounts
- Accounts with limited GPU usage history
- Educational/hackathon accounts with restricted resources

---

## ✅ Solutions

### Solution 1: Request Quota Increases (Recommended)

**For On-Demand Instances:**
1. Go to: https://console.aws.amazon.com/servicequotas/home?region=us-east-2
2. Search: "Running On-Demand G instances"
3. Request: 16-32 vCPUs (for 2-4 g5.2xlarge nodes)
4. Use case: "AI/ML inference workloads (NVIDIA NIM)"

**For Spot Instances:**
1. Same console, search: "Spot Instance Requests"
2. Request increase for g5.2xlarge
3. Or request general spot limit increase

**Approval Time:** Usually 1-4 hours (can be faster)

---

### Solution 2: Use Smaller Instance Type

Try `g5.xlarge` (4 vCPUs, 1 GPU) instead of `g5.2xlarge`:

```bash
eksctl create nodegroup \
  --cluster research-ops-cluster \
  --region us-east-2 \
  --name ng-gpu-small \
  --node-type g5.xlarge \
  --nodes 4 \
  --nodes-min 2 \
  --nodes-max 6 \
  --managed
```

**Pros:** May have quota available  
**Cons:** Less GPU memory per node, need more nodes

---

### Solution 3: Use CPU-Only Instances for Testing

For **testing the deployment** (without GPU NIMs), use CPU instances:

```bash
eksctl create nodegroup \
  --cluster research-ops-cluster \
  --region us-east-2 \
  --name ng-cpu-nodes \
  --node-type m5.2xlarge \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

**Note:** This allows testing the deployment, but NIMs won't have GPUs.

---

### Solution 4: Try Different Region

Some regions may have different quotas. Try **us-west-2** (Oregon):

```bash
# Delete current cluster
eksctl delete cluster --name research-ops-cluster --region us-east-2

# Update deploy.sh and secrets.yaml to use us-west-2
# Retry deployment
```

---

### Solution 5: Contact AWS Support

If quota requests are urgent:
1. Create support case: https://console.aws.amazon.com/support/home
2. Request expedited quota increase
3. Explain: "Hackathon project needs GPU instances immediately"

---

## 📋 Recommended Action Plan

### Immediate Steps (Next 30 minutes):

1. **Request On-Demand vCPU Quota Increase:**
   ```bash
   # Open browser
   open https://console.aws.amazon.com/servicequotas/home?region=us-east-2
   ```
   - Search: "Running On-Demand G instances"
   - Request: 16 vCPUs minimum
   - Submit

2. **Try Smaller Instance (g5.xlarge):**
   ```bash
   eksctl create nodegroup \
     --cluster research-ops-cluster \
     --region us-east-2 \
     --name ng-gpu-small \
     --node-type g5.xlarge \
     --nodes 4 \
     --nodes-min 2 \
     --nodes-max 6 \
     --managed
   ```

### If Quota Approved (1-4 hours):

1. Retry with g5.2xlarge:
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

2. Continue with deployment

---

## 🔍 Check Current Quotas

```bash
# Check On-Demand G instance quota
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region us-east-2 \
  --query 'Quota.Value'

# List all EC2 quotas
aws service-quotas list-service-quotas \
  --service-code ec2 \
  --region us-east-2 \
  --query 'Quotas[?contains(QuotaName, `vCPU`) || contains(QuotaName, `G instance`) || contains(QuotaName, `Spot`)].{Name:QuotaName,Code:QuotaCode,Value:Value}' \
  --output table
```

---

## 💡 Why This Happens

AWS implements quotas to:
- Prevent unexpected costs
- Manage resource availability
- Ensure fair usage

**New accounts** often have:
- vCPU limits: 0 for GPU instances
- Spot limits: Very low or 0
- Require explicit quota requests

**Hackathon accounts** may have:
- Even stricter limits
- Need approval process
- May require justification

---

## ⚡ Quick Test Option (CPU Only)

While waiting for GPU quota, test the deployment with CPU nodes:

```bash
# Create CPU nodegroup
eksctl create nodegroup \
  --cluster research-ops-cluster \
  --region us-east-2 \
  --name ng-cpu-test \
  --node-type m5.2xlarge \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed

# This will work for testing deployment
# NIMs will run but without GPU acceleration
```

---

**Current Status:** Both On-Demand and Spot instance attempts failed due to quota limits.  
**Action Required:** Request quota increases or use smaller/CPU instances for testing.


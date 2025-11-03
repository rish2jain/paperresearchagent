# 🚨 vCPU Limit Issue - Action Required

## ❌ Problem

The nodegroup creation failed due to **vCPU limit exceeded**:

```
VcpuLimitExceeded - You have requested more vCPU capacity than your current 
vCPU limit of 0 allows for the instance bucket that the specified instance type 
belongs to.
```

**Current Status:** 
- ❌ Nodegroup creation: FAILED
- ❌ CloudFormation: ROLLBACK_COMPLETE
- ⚠️ AWS Account vCPU limit for g5.2xlarge: **0**

---

## ✅ Solutions

### Option 1: Request vCPU Limit Increase (Recommended for Production)

**Steps:**

1. **Go to AWS Service Quotas:**
   ```bash
   # Open in browser
   https://console.aws.amazon.com/servicequotas/home?region=us-east-2
   ```

2. **Navigate to EC2 → Running On-Demand G instances:**
   - Search for: "Running On-Demand G instances"
   - Region: us-east-2
   - Current limit: 0
   - Request: At least 16 vCPUs (for 2x g5.2xlarge = 2 × 8 vCPUs)

3. **Request Increase:**
   - Click "Request quota increase"
   - New quota value: 16 (minimum) or 32 (recommended for scaling)
   - Use case: "GPU compute for AI/ML workloads (NVIDIA NIM inference)"
   - Submit request

4. **Wait for Approval:**
   - ⏱️ Usually approved within 1-4 hours
   - You'll receive an email when approved
   - Can check status in Service Quotas console

5. **After Approval, Retry:**
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

---

### Option 2: Use Spot Instances (Faster, May Help with Limits)

Spot instances sometimes have different quota limits. Try creating nodegroup with Spot:

```bash
eksctl create nodegroup \
  --cluster research-ops-cluster \
  --region us-east-2 \
  --name ng-gpu-nodes-spot \
  --node-type g5.2xlarge \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed \
  --spot
```

**Pros:**
- May bypass vCPU limits
- Lower cost (~70% discount)

**Cons:**
- Can be interrupted
- May not be available immediately

---

### Option 3: Use Smaller GPU Instance (If Available)

Try a smaller GPU instance that might have quota available:

```bash
# Try g5.xlarge (4 vCPUs, 1 GPU)
eksctl create nodegroup \
  --cluster research-ops-cluster \
  --region us-east-2 \
  --name ng-gpu-nodes-small \
  --node-type g5.xlarge \
  --nodes 4 \
  --nodes-min 2 \
  --nodes-max 6 \
  --managed
```

**Note:** This requires 16 vCPUs total (4 × 4), still needs quota increase if limit is 0.

---

### Option 4: Check Alternative Regions

Some regions may have different quotas. Try us-west-2:

```bash
# Delete current cluster
eksctl delete cluster --name research-ops-cluster --region us-east-2

# Update deploy.sh and secrets.yaml to use us-west-2
# Retry deployment
```

---

## 🔍 Check Current Quotas

```bash
# Check current vCPU limits
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region us-east-2 \
  --query 'Quota.{Service:ServiceCode,QuotaCode:QuotaCode,Value:Value,Adjustable:Adjustable}'

# List all EC2 quotas
aws service-quotas list-service-quotas \
  --service-code ec2 \
  --region us-east-2 \
  --query 'Quotas[?contains(QuotaName, `vCPU`) || contains(QuotaName, `G instance`)].{Name:QuotaName,Code:QuotaCode,Value:Value}' \
  --output table
```

---

## 📋 Recommended Action Plan

### Immediate (Next 30 minutes):

1. **Request vCPU Limit Increase** (if you can wait 1-4 hours)
   - Go to AWS Service Quotas console
   - Request increase for "Running On-Demand G instances"
   - Value: 16-32 vCPUs

2. **OR Try Spot Instances** (if you need it now)
   - Run the spot instance command above
   - Monitor for 10-15 minutes

### Once Quota Increased:

1. **Retry Nodegroup Creation:**
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

2. **Continue Deployment:**
   ```bash
   cd /Users/rish2jain/Documents/Hackathons/research-ops-agent/k8s
   NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
   export NGC_API_KEY
   ./deploy.sh
   ```

---

## 💡 Why This Happened

AWS accounts have default vCPU limits by instance family to prevent unexpected costs:
- **New accounts:** Often start with 0 vCPUs for GPU instances
- **G-family (GPU):** Typically requires explicit quota request
- **Different by region:** Each region has separate quotas

---

## ⚡ Quick Fix: Try Spot Instances Now

If you want to proceed immediately while waiting for quota approval:

```bash
eksctl create nodegroup \
  --cluster research-ops-cluster \
  --region us-east-2 \
  --name ng-gpu-nodes-spot \
  --node-type g5.2xlarge \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed \
  --spot
```

**This might work even with the vCPU limit, as Spot instances use different quotas.**

---

## 📞 AWS Support Links

- **Service Quotas Console:** https://console.aws.amazon.com/servicequotas
- **EC2 Limit Increase:** http://aws.amazon.com/contact-us/ec2-request
- **Support Case:** https://console.aws.amazon.com/support/home

---

**Status:** Waiting for vCPU quota increase or trying Spot instances as workaround.


# 💰 AWS Quota & Payment Guide

## ✅ Good News: Quota Increases are FREE!

**Key Points:**
- 🆓 **Requesting quota increases is FREE** - you only pay for resources you use
- ⚡ Most quota requests are approved automatically (minutes to hours)
- 💳 You pay for the EC2 instances when they run, not for the quota itself
- 🎯 For urgent requests, AWS Support can expedite (may require support plan)

---

## 📋 What You Need

Based on your deployment, you need these quotas in **us-east-2**:

### 1. **On-Demand G Instances (g5.2xlarge)**
- **Current Limit:** 0 vCPUs
- **Needed:** 16-32 vCPUs (for 2-4 nodes)
- **Cost if approved:** ~$1-2/hour for 2 nodes (only when running)

### 2. **Spot Instances (Optional - for cost savings)**
- **Current Limit:** Unknown/Exceeded
- **Needed:** Same as above
- **Cost if approved:** ~$0.30-0.60/hour (70% cheaper)

### 3. **Elastic IPs** (if needed)
- **Default Limit:** 5 per region
- **Usually:** Not an issue unless you have many running

---

## 🚀 How to Request Quota Increases

### Method 1: AWS Console (Recommended - FREE)

#### Step 1: Open Service Quotas Console
```bash
# Opens directly to your region
open https://console.aws.amazon.com/servicequotas/home?region=us-east-2
```

#### Step 2: Request On-Demand G Instance Quota

1. **Search for:** "Running On-Demand G instances"
   - Service: EC2
   - Quota Code: `L-DB2E81BA`

2. **Click "Request quota increase"**

3. **Fill in the form:**
   - **New quota value:** `32` (recommended) or `16` (minimum)
   - **Use case:** 
     ```
     AI/ML inference workloads using NVIDIA NIM containers.
     Deploying multi-agent research synthesis system on EKS cluster.
     Need 2-4 g5.2xlarge GPU nodes for production workloads.
     ```
   - **Contact method:** Email
   - **Submit**

4. **Wait for approval:**
   - ⏱️ **Usually:** 1-4 hours
   - ⚡ **Sometimes:** 15-30 minutes (automatic approval)
   - 📧 You'll get an email when approved

#### Step 3: Request Spot Instance Quota (Optional)

1. **Search for:** "All G and VT Spot Instance Requests"
   - Service: EC2
   - Quota Code: `L-34B43A08`

2. **Request increase:**
   - **New quota value:** `8` (for 4 spot instances)
   - **Use case:** Same as above
   - **Submit**

---

### Method 2: AWS CLI (FREE - Programmatic)

```bash
# Request On-Demand G instance quota increase
aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --desired-value 32 \
  --region us-east-2

# Request Spot instance quota increase
aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-34B43A08 \
  --desired-value 8 \
  --region us-east-2

# Check status
aws service-quotas get-requested-service-quota-change \
  --request-id <REQUEST_ID> \
  --region us-east-2
```

---

### Method 3: AWS Support (For Urgent Requests)

If you need **immediate** quota increases:

#### Support Plan Options:

1. **Basic Support** (FREE)
   - ⏱️ Response: 24 hours
   - ✅ Can request quota increases
   - ❌ No expedited processing

2. **Developer Support** ($29/month)
   - ⏱️ Response: 24 hours (email) or 1 hour (chat)
   - ✅ Can request expedited quota increases
   - ✅ Business hour support

3. **Business Support** ($100/month or 3-10% of usage)
   - ⏱️ Response: 1 hour (phone/chat)
   - ✅ Expedited quota increases
   - ✅ 24/7 support

#### Create Support Case:

1. Go to: https://console.aws.amazon.com/support/home
2. Click "Create case"
3. **Type:** Service limit increase
4. **Service:** EC2
5. **Limit type:** On-Demand instances
6. **Limit:** Running On-Demand G instances
7. **Region:** us-east-2
8. **New limit value:** 32
9. **Use case:** Same as above
10. **Urgency:** (Set based on your support plan)

---

## 💵 Cost Breakdown

### If Quotas Are Approved:

#### Scenario 1: 2x g5.2xlarge On-Demand
- **Per hour:** ~$1.00-1.20 per node = **$2.00-2.40/hour**
- **Per day:** ~$48-58/day (if running 24/7)
- **Per month:** ~$1,440-1,740/month

#### Scenario 2: 2x g5.2xlarge Spot
- **Per hour:** ~$0.30-0.40 per node = **$0.60-0.80/hour**
- **Per day:** ~$14-19/day (if running 24/7)
- **Per month:** ~$432-576/month

#### Scenario 3: Mixed (1 On-Demand + 1 Spot)
- **Per hour:** ~$1.30-1.60/hour
- **Per day:** ~$31-38/day
- **Per month:** ~$936-1,140/month

**Note:** You only pay when nodes are running. You can stop/delete nodes to save costs.

---

## ⚡ Fast-Track Options

### Option 1: Use AWS Credits (If You Have Them)

If you have AWS credits from:
- Hackathon/competition
- AWS Activate program
- AWS credits from partner

They apply automatically to usage. No special setup needed.

### Option 2: Try Different Regions

Some regions may have available quota:

```bash
# Check us-west-2 (Oregon) - often has better availability
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region us-west-2 \
  --query 'Quota.Value'

# If quota is available, you can deploy there instead
```

### Option 3: Start with Smaller Instances

Request quota for smaller instances first (faster approval):

```bash
# Request quota for g5.xlarge (4 vCPUs each)
# Then deploy with 4 smaller nodes instead of 2 large ones
```

---

## 🔍 Check Current Quota Status

```bash
# Check On-Demand G instance quota
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region us-east-2 \
  --query 'Quota.{Name:QuotaName,Value:Value,Adjustable:Adjustable}'

# Check pending requests
aws service-quotas list-requested-service-quota-change-history \
  --service-code ec2 \
  --region us-east-2 \
  --status PENDING \
  --query 'RequestedQuotas[].{Quota:QuotaName,Requested:DesiredValue,Status:Status}'

# List all EC2 quotas
aws service-quotas list-service-quotas \
  --service-code ec2 \
  --region us-east-2 \
  --query 'Quotas[?contains(QuotaName, `G instance`) || contains(QuotaName, `Spot`)].{Name:QuotaName,Code:QuotaCode,Value:Value,Adjustable:Adjustable}' \
  --output table
```

---

## 📋 Recommended Action Plan

### Right Now (Free Method):

1. **Request quota increase via console:**
   ```bash
   open https://console.aws.amazon.com/servicequotas/home?region=us-east-2
   ```
   - Request 32 vCPUs for On-Demand G instances
   - Use case: "AI/ML inference for hackathon project"

2. **Check status in 1-2 hours:**
   ```bash
   cd k8s
   ./check_quota_status.sh
   ```

3. **Once approved, run:**
   ```bash
   cd k8s
   ./auto_deploy_wait_quota.sh
   ```

### If You Need It Faster (Paid Option):

1. **Upgrade to Developer Support** ($29/month):
   - Get expedited quota processing
   - Can request urgent quota increases via chat
   - Cancel after deployment if not needed

2. **Or contact AWS Support:**
   - Explain it's for a hackathon
   - Request expedited approval
   - Many AWS Support reps are helpful with hackathon requests

---

## ❓ FAQ

**Q: Do I pay for the quota itself?**
A: No! Quota requests are free. You only pay for the EC2 instances when they run.

**Q: How long do quota approvals take?**
A: Usually 1-4 hours, sometimes as fast as 15-30 minutes for automatic approvals.

**Q: Can I get instant approval?**
A: Not guaranteed, but with AWS Support (paid plans), you can request expedited processing.

**Q: What if I'm on a tight budget?**
A: Use Spot instances - they're 70% cheaper. Just be aware they can be interrupted.

**Q: Can I use AWS credits?**
A: Yes! If you have credits, they automatically apply to your EC2 usage.

**Q: What's the minimum I can request?**
A: You can request as low as 8 vCPUs (1 g5.2xlarge node), but 16-32 is recommended for redundancy.

---

## 🎯 Quick Command Reference

```bash
# Request On-Demand G quota (32 vCPUs)
aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --desired-value 32 \
  --region us-east-2

# Check quota status
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region us-east-2

# Check pending requests
aws service-quotas list-requested-service-quota-change-history \
  --service-code ec2 \
  --region us-east-2 \
  --status PENDING
```

---

**Bottom Line:** You don't need to "pay" to get quotas - just request them (free) and wait for approval. You only pay for the compute resources you actually use. For urgent needs, AWS Support plans ($29-$100/month) can expedite the process.


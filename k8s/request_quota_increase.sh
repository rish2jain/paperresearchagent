#!/bin/bash

# Script to request AWS quota increases for EKS deployment
# This is FREE - you only pay for resources when they run

set -e

REGION="us-east-2"

echo "🚀 Requesting AWS Quota Increases"
echo "================================"
echo ""
echo "Note: Quota requests are FREE. You only pay for EC2 instances when they run."
echo ""

# Request On-Demand G instance quota increase
echo "📝 Requesting On-Demand G instance quota increase..."
echo "   Current limit: 0 vCPUs"
echo "   Requesting: 32 vCPUs (for 4x g5.2xlarge nodes)"
echo ""

ON_DEMAND_REQUEST=$(aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --desired-value 32 \
  --region "$REGION" \
  --output json)

ON_DEMAND_REQUEST_ID=$(echo "$ON_DEMAND_REQUEST" | jq -r '.RequestedQuota.RequestId')

if [ "$ON_DEMAND_REQUEST_ID" != "null" ] && [ -n "$ON_DEMAND_REQUEST_ID" ]; then
    echo "✅ On-Demand quota increase requested!"
    echo "   Request ID: $ON_DEMAND_REQUEST_ID"
    echo "   Status: PENDING"
    echo ""
else
    echo "⚠️  Could not create request. May already be pending or error occurred."
    echo "   Response: $ON_DEMAND_REQUEST"
    echo ""
fi

# Request Spot instance quota increase (optional, for cost savings)
echo "📝 Requesting Spot G instance quota increase (optional, for cost savings)..."
echo "   Requesting: 8 instances (for 4x g5.2xlarge spot nodes)"
echo ""

SPOT_REQUEST=$(aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-34B43A08 \
  --desired-value 8 \
  --region "$REGION" \
  --output json 2>/dev/null || echo '{"error": "Failed"}')

SPOT_REQUEST_ID=$(echo "$SPOT_REQUEST" | jq -r '.RequestedQuota.RequestId // empty' 2>/dev/null || echo "")

if [ -n "$SPOT_REQUEST_ID" ] && [ "$SPOT_REQUEST_ID" != "null" ]; then
    echo "✅ Spot quota increase requested!"
    echo "   Request ID: $SPOT_REQUEST_ID"
    echo "   Status: PENDING"
    echo ""
else
    echo "⚠️  Spot quota request may have failed or already exists"
    echo ""
fi

echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. Monitor approval status (usually 1-4 hours):"
echo "   aws service-quotas list-requested-service-quota-change-history \\"
echo "     --service-code ec2 \\"
echo "     --region $REGION \\"
echo "     --status PENDING"
echo ""
if [ -n "$ON_DEMAND_REQUEST_ID" ] && [ "$ON_DEMAND_REQUEST_ID" != "null" ]; then
    echo "2. Check specific request status:"
    echo "   aws service-quotas get-requested-service-quota-change \\"
    echo "     --request-id $ON_DEMAND_REQUEST_ID \\"
    echo "     --region $REGION"
    echo ""
fi
echo "3. Once approved, run deployment:"
echo "   cd k8s && ./auto_deploy_wait_quota.sh"
echo ""
echo "4. Or manually create nodegroup:"
echo "   eksctl create nodegroup \\"
echo "     --cluster research-ops-cluster \\"
echo "     --region $REGION \\"
echo "     --name ng-gpu-nodes \\"
echo "     --node-type g5.2xlarge \\"
echo "     --nodes 2 \\"
echo "     --nodes-min 1 \\"
echo "     --nodes-max 3 \\"
echo "     --managed"
echo ""
echo "💰 Cost Estimates:"
echo "   - On-Demand: ~$2-2.40/hour (2 nodes)"
echo "   - Spot: ~$0.60-0.80/hour (70% cheaper)"
echo "   - You only pay when nodes are running"
echo ""
echo "✅ Quota requests submitted! Check your email for approval notifications."


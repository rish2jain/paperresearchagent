#!/bin/bash

# Script to check AWS quota increase request status

REGION="us-east-2"
ON_DEMAND_REQUEST_ID="d2c3a82bb47b4dcc912c9c51cbc68ed4staMBCb4"
SPOT_REQUEST_ID="5eddd4c9b5ed48359d5872de12828474SfMFXF1I"

echo "🔍 Checking AWS Quota Increase Request Status"
echo "Region: $REGION"
echo ""

echo "1️⃣  On-Demand G Instances Request:"
aws service-quotas get-requested-service-quota-change \
  --request-id "$ON_DEMAND_REQUEST_ID" \
  --region "$REGION" \
  --query 'RequestedQuota.{Quota:QuotaName,Desired:DesiredValue,Current:Value,Status:Status,CaseId:CaseId}' \
  --output json 2>&1

echo ""
echo "2️⃣  Spot G Instances Request:"
aws service-quotas get-requested-service-quota-change \
  --request-id "$SPOT_REQUEST_ID" \
  --region "$REGION" \
  --query 'RequestedQuota.{Quota:QuotaName,Desired:DesiredValue,Current:Value,Status:Status,CaseId:CaseId}' \
  --output json 2>&1

echo ""
echo "📋 Current Quota Values:"
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-DB2E81BA \
  --region "$REGION" \
  --query 'Quota.{Name:QuotaName,Value:Value}' \
  --output json 2>&1

echo ""
echo "💡 Once Status changes to 'APPROVED', you can proceed with nodegroup creation."
echo "   Run this script periodically to check: ./check_quota_status.sh"


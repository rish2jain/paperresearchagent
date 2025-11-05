#!/bin/bash
# Add g5.4xlarge node group for Reasoning NIM
# This provides 64GB RAM needed for TensorRT compilation

set -e

echo "🚀 Adding g5.4xlarge Node Group for Reasoning NIM"
echo "=================================================="

CLUSTER_NAME="research-ops-cluster"
REGION="us-east-2"
NODEGROUP_NAME="gpu-nodes-large"
INSTANCE_TYPE="g5.4xlarge"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if nodegroup already exists
if eksctl get nodegroup --cluster "$CLUSTER_NAME" --region "$REGION" --name "$NODEGROUP_NAME" &>/dev/null; then
    echo -e "${YELLOW}Nodegroup $NODEGROUP_NAME already exists${NC}"
    echo "Checking status..."
    eksctl get nodegroup --cluster "$CLUSTER_NAME" --region "$REGION" --name "$NODEGROUP_NAME"
    exit 0
fi

# Create nodegroup
echo -e "${YELLOW}Creating nodegroup: $NODEGROUP_NAME${NC}"
echo "Instance Type: $INSTANCE_TYPE"
echo "Memory: 64GB (sufficient for TensorRT compilation)"
echo "This will take 10-15 minutes..."
echo ""

eksctl create nodegroup \
    --cluster "$CLUSTER_NAME" \
    --region "$REGION" \
    --name "$NODEGROUP_NAME" \
    --node-type "$INSTANCE_TYPE" \
    --nodes 1 \
    --nodes-min 1 \
    --nodes-max 2 \
    --managed \
    --node-labels "instance-type=large,workload-type=reasoning-nim"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Nodegroup created successfully!${NC}"
    echo ""
    echo "Waiting for nodes to be ready..."
    sleep 30
    
    # Wait for nodes
    echo "Checking node status..."
    kubectl get nodes -l instance-type=large
    
    echo ""
    echo -e "${GREEN}Next steps:${NC}"
    echo "1. Update reasoning-nim-deployment.yaml to use nodeSelector:"
    echo "   nodeSelector:"
    echo "     instance-type: large"
    echo ""
    echo "2. Apply the updated deployment:"
    echo "   kubectl apply -f k8s/reasoning-nim-deployment.yaml"
    echo ""
    echo "3. The pod should now have sufficient memory (64GB)"
else
    echo -e "${RED}❌ Failed to create nodegroup${NC}"
    echo "Check AWS quotas: https://console.aws.amazon.com/servicequotas"
    echo "You may need to request quota increase for g5.4xlarge"
    exit 1
fi

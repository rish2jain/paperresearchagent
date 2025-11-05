#!/bin/bash
# Monitor nodegroup creation progress

CLUSTER_NAME="research-ops-cluster"
REGION="us-east-2"
NODEGROUP_NAME="gpu-nodes-large"

echo "🔍 Monitoring Node Group Creation..."
echo "===================================="
echo ""

while true; do
    STATUS=$(eksctl get nodegroup --cluster "$CLUSTER_NAME" --region "$REGION" --name "$NODEGROUP_NAME" --output json 2>/dev/null | grep -o '"Status":"[^"]*"' | cut -d'"' -f4 || echo "UNKNOWN")
    
    echo "[$(date +%H:%M:%S)] Status: $STATUS"
    
    if [ "$STATUS" = "ACTIVE" ]; then
        echo ""
        echo "✅ Nodegroup is ACTIVE!"
        echo ""
        kubectl get nodes -l instance-type=large
        echo ""
        echo "Next: Apply updated Reasoning NIM deployment:"
        echo "  kubectl apply -f k8s/reasoning-nim-deployment.yaml"
        break
    elif [ "$STATUS" = "CREATE_FAILED" ] || [ "$STATUS" = "DELETE_IN_PROGRESS" ]; then
        echo ""
        echo "❌ Nodegroup creation failed or was deleted"
        echo "Check CloudFormation events for details"
        break
    fi
    
    sleep 30
done

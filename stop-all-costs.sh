#!/bin/bash
# Script to stop all AWS costs by deleting EKS cluster and all resources

set -e

CLUSTER_NAME="research-ops-cluster"
REGION="us-east-2"
NAMESPACE="research-ops"

echo "=========================================="
echo "🚨 STOPPING ALL AWS COSTS"
echo "=========================================="
echo ""
echo "This will delete:"
echo "  • EKS Cluster: ${CLUSTER_NAME}"
echo "  • All node groups (EC2 instances)"
echo "  • All Kubernetes resources"
echo "  • Control plane (~$0.10/hour)"
echo "  • EC2 instances (~$1-2/hour each)"
echo ""
echo "Estimated cost savings: ~$2-3/hour (~$1,500-2,000/month)"
echo ""
read -p "Type 'DELETE ALL' to confirm: " confirm

if [ "$confirm" != "DELETE ALL" ]; then
    echo "❌ Cancelled - confirmation text did not match"
    exit 1
fi

echo ""
echo "🗑️  Starting cleanup..."

# Step 1: Update kubeconfig
echo "1. Updating kubeconfig..."
aws eks update-kubeconfig --name "${CLUSTER_NAME}" --region "${REGION}" 2>/dev/null || {
    echo "⚠️  Could not update kubeconfig - cluster may already be deleted"
}

# Step 2: Delete LoadBalancer services first (if any)
echo "2. Checking for LoadBalancer services..."
if kubectl get svc -n "${NAMESPACE}" 2>/dev/null | grep -q LoadBalancer; then
    echo "   Found LoadBalancer services - deleting..."
    kubectl get svc -n "${NAMESPACE}" -o json | jq -r '.items[] | select(.spec.type=="LoadBalancer") | .metadata.name' | while read svc; do
        echo "   Deleting service: ${svc}"
        kubectl delete svc "${svc}" -n "${NAMESPACE}" || true
    done
    echo "   Waiting for LoadBalancers to be released..."
    sleep 10
else
    echo "   No LoadBalancer services found"
fi

# Step 3: Delete namespace (removes all K8s resources)
echo "3. Deleting namespace ${NAMESPACE}..."
if kubectl get namespace "${NAMESPACE}" 2>/dev/null; then
    kubectl delete namespace "${NAMESPACE}" --wait=true --timeout=300s || {
        echo "⚠️  Namespace deletion timed out or failed, but continuing..."
    }
    echo "   ✅ Namespace deleted"
else
    echo "   ⚠️  Namespace not found (may already be deleted)"
fi

# Step 4: Delete EKS cluster
echo "4. Deleting EKS cluster ${CLUSTER_NAME}..."
if eksctl get cluster --name "${CLUSTER_NAME}" --region "${REGION}" 2>/dev/null | grep -q "${CLUSTER_NAME}"; then
    eksctl delete cluster \
        --name "${CLUSTER_NAME}" \
        --region "${REGION}" \
        --wait
    echo "   ✅ Cluster deletion initiated"
else
    echo "   ⚠️  Cluster not found (may already be deleted)"
fi

echo ""
echo "=========================================="
echo "✅ CLEANUP COMPLETE"
echo "=========================================="
echo ""
echo "All AWS resources have been deleted."
echo "Costs should stop immediately."
echo ""
echo "To verify:"
echo "  aws eks list-clusters --region ${REGION}"
echo "  aws ec2 describe-instances --region ${REGION} --filters 'Name=tag:eks:cluster-name,Values=${CLUSTER_NAME}'"
echo ""



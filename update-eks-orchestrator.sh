#!/bin/bash

# Update EKS Agent Orchestrator with Latest Code
# This script rebuilds and redeploys the orchestrator with the bug fix

set -e

echo "🔨 Building updated orchestrator Docker image..."
docker build -f Dockerfile.orchestrator -t 294337990007.dkr.ecr.us-east-2.amazonaws.com/research-ops/orchestrator:latest .

echo "📦 Pushing updated image to ECR..."
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 294337990007.dkr.ecr.us-east-2.amazonaws.com
docker push 294337990007.dkr.ecr.us-east-2.amazonaws.com/research-ops/orchestrator:latest

echo "🔄 Restarting agent-orchestrator pod to pull new image..."
kubectl delete pod -n research-ops -l app=agent-orchestrator

echo "⏳ Waiting for new pod to start..."
kubectl wait --for=condition=ready pod -l app=agent-orchestrator -n research-ops --timeout=120s

echo "✅ Agent orchestrator updated successfully!"
echo ""
echo "📊 Check pod status:"
kubectl get pods -n research-ops -l app=agent-orchestrator

echo ""
echo "📝 View logs:"
echo "kubectl logs -n research-ops -l app=agent-orchestrator --tail=50"

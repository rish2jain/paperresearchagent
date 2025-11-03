#!/bin/bash
# Script to build and push container images to ECR for research-ops-agent

set -e  # Exit on error

# Configuration
REGION="us-east-2"
ORCHESTRATOR_REPO="research-ops/orchestrator"
UI_REPO="research-ops/ui"

echo "🚀 Starting ECR deployment process..."

# Step 1: Get AWS account ID and region
echo "📋 Step 1: Getting AWS account ID..."
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "❌ Error: Could not get AWS account ID. Make sure AWS CLI is configured."
    exit 1
fi
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com"
echo "✅ AWS Account ID: $AWS_ACCOUNT_ID"
echo "✅ ECR Registry: $ECR_REGISTRY"

# Step 2: Create ECR repositories
echo ""
echo "📋 Step 2: Creating ECR repositories..."
for repo in "$ORCHESTRATOR_REPO" "$UI_REPO"; do
    echo "  Creating repository: $repo"
    if aws ecr describe-repositories --repository-names "$repo" --region "$REGION" &>/dev/null; then
        echo "  ✅ Repository $repo already exists"
    else
        aws ecr create-repository --repository-name "$repo" --region "$REGION" || {
            echo "  ⚠️  Repository creation failed or already exists"
        }
        echo "  ✅ Repository $repo created"
    fi
done

# Step 3: Login to ECR
echo ""
echo "📋 Step 3: Logging in to ECR..."
aws ecr get-login-password --region "$REGION" | \
    docker login --username AWS --password-stdin "$ECR_REGISTRY" || {
    echo "❌ Error: Failed to login to ECR"
    exit 1
}
echo "✅ Successfully logged in to ECR"

# Step 4: Setup buildx for multi-platform builds
echo ""
echo "📋 Step 4: Setting up Docker buildx for Linux AMD64..."
docker buildx create --use --name multiplatform-builder 2>/dev/null || docker buildx use multiplatform-builder
docker buildx inspect --bootstrap || true

# Step 5: Build and push orchestrator
echo ""
echo "📋 Step 5: Building and pushing orchestrator image (linux/amd64)..."
ORCHESTRATOR_IMAGE="${ECR_REGISTRY}/${ORCHESTRATOR_REPO}:latest"
echo "  Building: $ORCHESTRATOR_IMAGE"
docker buildx build --platform linux/amd64 -f Dockerfile.orchestrator -t "$ORCHESTRATOR_IMAGE" --push . || {
    echo "❌ Error: Failed to build orchestrator image"
    exit 1
}
echo "✅ Orchestrator image built and pushed successfully"

# Step 6: Build and push UI
echo ""
echo "📋 Step 6: Building and pushing UI image (linux/amd64)..."
UI_IMAGE="${ECR_REGISTRY}/${UI_REPO}:latest"
echo "  Building: $UI_IMAGE"
docker buildx build --platform linux/amd64 -f Dockerfile.ui -t "$UI_IMAGE" --push . || {
    echo "❌ Error: Failed to build UI image"
    exit 1
}
echo "✅ UI image built and pushed successfully"

# Step 7: Update deployment manifests
echo ""
echo "📋 Step 7: Updating deployment manifests..."

# Update orchestrator deployment
sed -i.bak "s|YOUR_REGISTRY/research-ops-agent:latest|${ORCHESTRATOR_IMAGE}|g" \
    k8s/agent-orchestrator-deployment.yaml

# Verify orchestrator replacement
if grep -q "YOUR_REGISTRY/research-ops-agent:latest" k8s/agent-orchestrator-deployment.yaml; then
    echo "❌ Error: Failed to replace orchestrator image placeholder in agent-orchestrator-deployment.yaml"
    exit 1
fi
if ! grep -q "${ORCHESTRATOR_IMAGE}" k8s/agent-orchestrator-deployment.yaml; then
    echo "❌ Error: New orchestrator image not found in agent-orchestrator-deployment.yaml after replacement"
    exit 1
fi

# Update UI deployment
sed -i.bak "s|YOUR_REGISTRY/research-ops-ui:latest|${UI_IMAGE}|g" \
    k8s/web-ui-deployment.yaml

# Verify UI replacement
if grep -q "YOUR_REGISTRY/research-ops-ui:latest" k8s/web-ui-deployment.yaml; then
    echo "❌ Error: Failed to replace UI image placeholder in web-ui-deployment.yaml"
    exit 1
fi
if ! grep -q "${UI_IMAGE}" k8s/web-ui-deployment.yaml; then
    echo "❌ Error: New UI image not found in web-ui-deployment.yaml after replacement"
    exit 1
fi

echo "✅ Deployment manifests updated and verified"

# Step 7: Display summary
echo ""
echo "✅ Deployment Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "ECR Registry:     $ECR_REGISTRY"
echo "Orchestrator:     $ORCHESTRATOR_IMAGE"
echo "UI:               $UI_IMAGE"
echo ""
echo "📝 Next steps:"
echo "1. Review the updated deployment manifests:"
echo "   - k8s/agent-orchestrator-deployment.yaml"
echo "   - k8s/web-ui-deployment.yaml"
echo ""
echo "2. Re-apply deployments:"
echo "   kubectl apply -f k8s/agent-orchestrator-deployment.yaml"
echo "   kubectl apply -f k8s/web-ui-deployment.yaml"
echo ""
echo "3. Verify pods are running:"
echo "   kubectl get pods -n research-ops -w"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"


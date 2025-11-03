#!/bin/bash

# Automated script to monitor quota approval and continue deployment
# This script will wait for quota approval, then create nodegroup and deploy services

set -e  # Exit on error

REGION="us-east-2"
CLUSTER_NAME="research-ops-cluster"
ON_DEMAND_REQUEST_ID="d2c3a82bb47b4dcc912c9c51cbc68ed4staMBCb4"
SPOT_REQUEST_ID="5eddd4c9b5ed48359d5872de12828474SfMFXF1I"
NODEGROUP_NAME="ng-gpu-nodes"
CHECK_INTERVAL=300  # Check every 5 minutes (300 seconds)
MAX_WAIT_HOURS=6    # Maximum wait time: 6 hours
MAX_CHECKS=$((MAX_WAIT_HOURS * 60 / 5))  # Convert to number of checks

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# Function to check quota request status
check_quota_status() {
    local request_id=$1
    local quota_name=$(aws service-quotas get-requested-service-quota-change \
        --request-id "$request_id" \
        --region "$REGION" \
        --query 'RequestedQuota.Status' \
        --output text 2>/dev/null)
    
    echo "$quota_name"
}

# Function to check if quota is approved
is_quota_approved() {
    local on_demand_status=$(check_quota_status "$ON_DEMAND_REQUEST_ID")
    local spot_status=$(check_quota_status "$SPOT_REQUEST_ID")
    
    if [ "$on_demand_status" = "APPROVED" ]; then
        return 0  # At least On-Demand is approved (this is what we need)
    fi
    return 1
}

# Function to get current quota value
get_current_quota() {
    aws service-quotas get-service-quota \
        --service-code ec2 \
        --quota-code L-DB2E81BA \
        --region "$REGION" \
        --query 'Quota.Value' \
        --output text 2>/dev/null || echo "0"
}

# Function to wait for quota approval
wait_for_quota_approval() {
    info "Monitoring quota approval status..."
    info "Checking every 5 minutes (max wait: $MAX_WAIT_HOURS hours)"
    echo ""
    
    local check_count=0
    
    while [ $check_count -lt $MAX_CHECKS ]; do
        check_count=$((check_count + 1))
        
        # Check On-Demand quota status
        local on_demand_status=$(check_quota_status "$ON_DEMAND_REQUEST_ID")
        local spot_status=$(check_quota_status "$SPOT_REQUEST_ID")
        local current_quota=$(get_current_quota)
        
        info "[Check $check_count/$MAX_CHECKS] $(date '+%Y-%m-%d %H:%M:%S')"
        echo "   On-Demand G instances: Status=$on_demand_status, Current quota=$current_quota vCPUs"
        echo "   Spot G instances: Status=$spot_status"
        echo ""
        
        # Check if On-Demand is approved
        if [ "$on_demand_status" = "APPROVED" ]; then
            success "On-Demand quota is APPROVED!"
            local new_quota=$(get_current_quota)
            info "New quota value: $new_quota vCPUs"
            
            # Verify quota is sufficient (should be >= 16)
            if (( $(echo "$new_quota >= 16" | bc -l) )); then
                success "Quota is sufficient for 2x g5.2xlarge nodes (16 vCPUs)"
                return 0
            else
                warning "Quota approved but value ($new_quota) is less than requested. Proceeding anyway..."
                return 0
            fi
        elif [ "$on_demand_status" = "DENIED" ]; then
            error "Quota request was DENIED. Please check AWS console or contact support."
            exit 1
        elif [ "$on_demand_status" = "CASE_CLOSED" ]; then
            error "Quota request case was closed. Please check AWS console."
            exit 1
        fi
        
        # Wait before next check
        if [ $check_count -lt $MAX_CHECKS ]; then
            info "Waiting $((CHECK_INTERVAL / 60)) minutes before next check..."
            sleep $CHECK_INTERVAL
        fi
    done
    
    error "Maximum wait time ($MAX_WAIT_HOURS hours) exceeded. Quota may still be pending."
    error "Please check manually: ./check_quota_status.sh"
    exit 1
}

# Function to create nodegroup
create_nodegroup() {
    info "Creating nodegroup: $NODEGROUP_NAME"
    info "This will take 10-15 minutes..."
    echo ""
    
    eksctl create nodegroup \
        --cluster "$CLUSTER_NAME" \
        --region "$REGION" \
        --name "$NODEGROUP_NAME" \
        --node-type g5.2xlarge \
        --nodes 2 \
        --nodes-min 1 \
        --nodes-max 3 \
        --managed
    
    if [ $? -eq 0 ]; then
        success "Nodegroup created successfully!"
        return 0
    else
        error "Failed to create nodegroup. Check logs above."
        exit 1
    fi
}

# Function to verify nodegroup is ready
verify_nodegroup() {
    info "Verifying nodegroup is ACTIVE..."
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        attempt=$((attempt + 1))
        local status=$(aws eks describe-nodegroup \
            --cluster-name "$CLUSTER_NAME" \
            --nodegroup-name "$NODEGROUP_NAME" \
            --region "$REGION" \
            --query 'nodegroup.status' \
            --output text 2>/dev/null || echo "NOT_FOUND")
        
        info "[$attempt/$max_attempts] Nodegroup status: $status"
        
        if [ "$status" = "ACTIVE" ]; then
            success "Nodegroup is ACTIVE and ready!"
            
            # Verify nodes are visible
            info "Verifying nodes are visible in cluster..."
            aws eks update-kubeconfig --name "$CLUSTER_NAME" --region "$REGION" > /dev/null 2>&1
            
            local node_count=$(kubectl get nodes --no-headers 2>/dev/null | wc -l | tr -d ' ')
            if [ "$node_count" -gt 0 ]; then
                success "Found $node_count node(s) in cluster"
                kubectl get nodes
                return 0
            else
                warning "Nodes not yet visible. This is normal - may take a few more minutes."
                sleep 60
                continue
            fi
        elif [ "$status" = "CREATE_FAILED" ] || [ "$status" = "FAILED" ]; then
            error "Nodegroup creation failed!"
            exit 1
        fi
        
        sleep 30
    done
    
    warning "Nodegroup still in CREATING status after $max_attempts checks. Proceeding with deployment..."
    return 0
}

# Function to continue with deployment
continue_deployment() {
    info "Continuing with service deployment..."
    echo ""
    
    # Change to k8s directory
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$script_dir"
    
    # Get NGC API key
    if [ -f "secrets.yaml" ]; then
        export NGC_API_KEY=$(grep "NGC_API_KEY" secrets.yaml | head -1 | sed 's/.*NGC_API_KEY: "\(.*\)"/\1/')
        if [ -z "$NGC_API_KEY" ]; then
            error "NGC_API_KEY not found in secrets.yaml"
            exit 1
        fi
        success "NGC_API_KEY loaded"
    else
        error "secrets.yaml not found in $(pwd)"
        exit 1
    fi
    
    # Update kubeconfig
    info "Updating kubeconfig..."
    aws eks update-kubeconfig --name "$CLUSTER_NAME" --region "$REGION"
    
    # Apply Kubernetes manifests
    info "Applying Kubernetes manifests..."
    
    local manifests=(
        "namespace.yaml"
        "secrets.yaml"
        "reasoning-nim-deployment.yaml"
        "embedding-nim-deployment.yaml"
        "vector-db-deployment.yaml"
        "agent-orchestrator-deployment.yaml"
        "web-ui-deployment.yaml"
        "ingress.yaml"
    )
    
    for manifest in "${manifests[@]}"; do
        if [ -f "$manifest" ]; then
            info "Applying $manifest..."
            kubectl apply -f "$manifest"
        else
            warning "$manifest not found, skipping..."
        fi
    done
    
    success "All manifests applied!"
    echo ""
    
    # Wait for pods to be ready
    info "Waiting for pods to be ready (this may take 5-10 minutes)..."
    echo ""
    
    kubectl wait --for=condition=ready pod -l app=reasoning-nim -n research-ops --timeout=600s || warning "Reasoning NIM not ready yet"
    kubectl wait --for=condition=ready pod -l app=embedding-nim -n research-ops --timeout=600s || warning "Embedding NIM not ready yet"
    kubectl wait --for=condition=ready pod -l app=vector-db -n research-ops --timeout=600s || warning "Vector DB not ready yet"
    kubectl wait --for=condition=ready pod -l app=agent-orchestrator -n research-ops --timeout=600s || warning "Agent orchestrator not ready yet"
    kubectl wait --for=condition=ready pod -l app=web-ui -n research-ops --timeout=600s || warning "Web UI not ready yet"
    
    echo ""
    info "Checking pod status..."
    kubectl get pods -n research-ops
    
    echo ""
    success "Deployment complete!"
    echo ""
    info "Getting service endpoints..."
    echo ""
    
    # Get ingress URL
    local ingress_url=$(kubectl get ingress -n research-ops -o jsonpath='{.items[0].status.loadBalancer.ingress[0].hostname}' 2>/dev/null || echo "N/A")
    
    echo "📋 Service Information:"
    echo "   Cluster: $CLUSTER_NAME"
    echo "   Region: $REGION"
    echo "   Ingress URL: $ingress_url"
    echo ""
    echo "🧪 Test the deployment:"
    echo "   curl http://$ingress_url/health"
    echo ""
    echo "📊 Monitor pods:"
    echo "   kubectl get pods -n research-ops -w"
    echo ""
    echo "📝 View logs:"
    echo "   kubectl logs -n research-ops -l app=agent-orchestrator -f"
}

# Main execution
main() {
    echo "🚀 Automated Deployment Script"
    echo "================================"
    echo ""
    echo "This script will:"
    echo "1. Monitor quota approval status"
    echo "2. Create nodegroup when quota is approved"
    echo "3. Verify nodegroup is ready"
    echo "4. Deploy all Kubernetes services"
    echo ""
    echo "Cluster: $CLUSTER_NAME"
    echo "Region: $REGION"
    echo ""
    
    # Step 1: Wait for quota approval
    wait_for_quota_approval
    
    # Step 2: Create nodegroup
    create_nodegroup
    
    # Step 3: Verify nodegroup
    verify_nodegroup
    
    # Step 4: Continue deployment
    continue_deployment
    
    success "🎉 All done! Your ResearchOps Agent is deployed!"
}

# Run main function
main "$@"


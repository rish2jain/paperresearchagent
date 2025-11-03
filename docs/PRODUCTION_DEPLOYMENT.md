# Production Deployment Guide

**Last Updated**: 2025-01-27  
**Version**: 1.0

---

## Overview

This guide covers the complete production deployment process for ResearchOps Agent on AWS EKS, including prerequisites, step-by-step instructions, and post-deployment validation.

---

## Prerequisites

### 1. AWS Account Setup
- AWS account with admin access
- AWS CLI configured (`aws configure`)
- kubectl installed (v1.28+)
- eksctl installed (latest)
- Docker installed

### 2. Required AWS Services
- **EKS Cluster**: Kubernetes 1.28+
- **ECR**: Container registry
- **S3**: Backup storage
- **IAM**: Service roles and policies
- **VPC**: Network configuration

### 3. Required Secrets & Configuration
- NVIDIA API keys (if using cloud NIMs)
- Paper source API keys (Semantic Scholar, IEEE, etc.)
- Redis URL (if using external Redis)
- Domain name and SSL certificates (for ingress)

---

## Step 1: Infrastructure Setup

### 1.1 Create EKS Cluster

```bash
# Create cluster configuration
cat > cluster-config.yaml <<EOF
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: research-ops-prod
  region: us-east-1
  version: "1.28"

vpc:
  cidr: "10.0.0.0/16"

nodeGroups:
  - name: ng-1
    instanceType: m5.large
    desiredCapacity: 3
    minSize: 2
    maxSize: 5
    volumeSize: 50
    ssh:
      allow: false

managedNodeGroups:
  - name: ng-spot
    instanceTypes: ["m5.large", "m5.xlarge"]
    spot: true
    desiredCapacity: 2
    minSize: 1
    maxSize: 4
EOF

# Create cluster
eksctl create cluster -f cluster-config.yaml

# Configure kubectl
aws eks update-kubeconfig --name research-ops-prod --region us-east-1
```

### 1.2 Create S3 Bucket for Backups

```bash
# Create backup bucket
aws s3 mb s3://research-ops-backups-prod --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket research-ops-backups-prod \
  --versioning-configuration Status=Enabled

# Enable encryption
aws s3api put-bucket-encryption \
  --bucket research-ops-backups-prod \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

### 1.3 Create ECR Repositories

```bash
# Create repositories for each service
aws ecr create-repository --repository-name research-ops/orchestrator
aws ecr create-repository --repository-name research-ops/ui
aws ecr create-repository --repository-name research-ops/mock-reasoning
aws ecr create-repository --repository-name research-ops/mock-embedding
```

---

## Step 2: Build and Push Docker Images

### 2.1 Build Images

```bash
# Set ECR registry
ECR_REGISTRY=$(aws ecr describe-repositories --query 'repositories[0].repositoryUri' --output text | cut -d'/' -f1)

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin $ECR_REGISTRY

# Build and push orchestrator
docker build -f Dockerfile.orchestrator -t $ECR_REGISTRY/research-ops/orchestrator:latest .
docker push $ECR_REGISTRY/research-ops/orchestrator:latest

# Build and push UI
docker build -f Dockerfile.ui -t $ECR_REGISTRY/research-ops/ui:latest .
docker push $ECR_REGISTRY/research-ops/ui:latest

# Build and push mock services (if using)
docker build -f Dockerfile.mock-reasoning-nim -t $ECR_REGISTRY/research-ops/mock-reasoning:latest .
docker push $ECR_REGISTRY/research-ops/mock-reasoning:latest

docker build -f Dockerfile.mock-embedding-nim -t $ECR_REGISTRY/research-ops/mock-embedding:latest .
docker push $ECR_REGISTRY/research-ops/mock-embedding:latest
```

### 2.2 Update Deployment Manifests

Update image references in `k8s/*-deployment.yaml` files:

```bash
# Replace image references
sed -i "s|IMAGE_PLACEHOLDER|$ECR_REGISTRY/research-ops/orchestrator:latest|g" \
  k8s/agent-orchestrator-deployment.yaml
```

---

## Step 3: Configure Secrets

### 3.1 Create Kubernetes Secrets

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets from template
cp k8s/secrets.yaml.template k8s/secrets.yaml

# Edit secrets.yaml with actual values
# Then apply:
kubectl apply -f k8s/secrets.yaml

# Verify secrets
kubectl get secrets -n research-ops
```

### 3.2 Configure Environment Variables

Update deployment files with production environment variables:

```yaml
# Example: k8s/agent-orchestrator-deployment.yaml
env:
  - name: REASONING_NIM_URL
    value: "http://reasoning-nim.research-ops.svc.cluster.local:8000"
  - name: EMBEDDING_NIM_URL
    value: "http://embedding-nim.research-ops.svc.cluster.local:8001"
  - name: DEMO_MODE
    value: "false"
  - name: LOG_LEVEL
    value: "info"
  - name: CIRCUIT_BREAKER_FAIL_MAX
    value: "5"
  - name: CIRCUIT_BREAKER_TIMEOUT
    value: "60"
  - name: RATE_LIMIT_DEFAULT
    value: "100"
  - name: REDIS_URL
    valueFrom:
      secretKeyRef:
        name: research-ops-secrets
        key: redis-url
resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: 2000m
    memory: 4Gi
```

---

## Step 4: Deploy Services

### 4.1 Deploy in Dependency Order

```bash
# 1. Vector Database (Qdrant)
kubectl apply -f k8s/vector-db-deployment.yaml

# Wait for Qdrant to be ready
kubectl wait --for=condition=ready pod -l app=qdrant -n research-ops --timeout=300s

# 2. Redis (if not using external)
# kubectl apply -f k8s/redis-deployment.yaml

# 3. NIM Services
kubectl apply -f k8s/reasoning-nim-deployment.yaml
kubectl apply -f k8s/embedding-nim-deployment.yaml

# Wait for NIMs to be ready
kubectl wait --for=condition=ready pod -l app=reasoning-nim -n research-ops --timeout=300s
kubectl wait --for=condition=ready pod -l app=embedding-nim -n research-ops --timeout=300s

# 4. Agent Orchestrator
kubectl apply -f k8s/agent-orchestrator-deployment.yaml

# 5. Web UI
kubectl apply -f k8s/web-ui-deployment.yaml

# 6. Ingress
kubectl apply -f k8s/ingress.yaml
```

### 4.2 Verify Deployments

```bash
# Check all pods are running
kubectl get pods -n research-ops

# Check services
kubectl get svc -n research-ops

# Check ingress
kubectl get ingress -n research-ops

# View logs
kubectl logs -f deployment/agent-orchestrator -n research-ops
```

---

## Step 5: Configure Ingress and DNS

### 5.1 Install Ingress Controller

```bash
# Install AWS Load Balancer Controller
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=research-ops-prod \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

### 5.2 Configure DNS

```bash
# Get ingress external IP
INGRESS_IP=$(kubectl get ingress research-ops-ingress -n research-ops \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Update DNS records (example for Route53)
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456789 \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "api.research-ops.example.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "'$INGRESS_IP'"}]
      }
    }]
  }'
```

---

## Step 6: Post-Deployment Validation

### 6.1 Health Checks

```bash
# API health check
curl https://api.research-ops.example.com/health

# UI health check
curl https://ui.research-ops.example.com/

# Individual service health
kubectl exec -n research-ops deployment/agent-orchestrator -- \
  curl http://localhost:8080/health
```

### 6.2 Run Integration Tests

```bash
# Run comprehensive integration tests
cd /path/to/research-ops-agent
pytest src/test_comprehensive_integration.py -v

# Run existing integration tests
python src/test_integration.py
```

### 6.3 Smoke Tests

```bash
# Test research endpoint
curl -X POST https://api.research-ops.example.com/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning",
    "max_papers": 3
  }'

# Verify response structure
curl -X POST https://api.research-ops.example.com/research \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "max_papers": 1}' | \
  jq '.papers_analyzed, .decisions, .common_themes'
```

---

## Step 7: Monitoring Setup

### 7.1 Install Prometheus and Grafana

```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d

# Install Grafana
# (Included with kube-prometheus-stack)
```

### 7.2 Configure ServiceMonitors

```yaml
# k8s/monitoring/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: research-ops-metrics
  namespace: research-ops
spec:
  selector:
    matchLabels:
      app: agent-orchestrator
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
```

Apply:
```bash
kubectl apply -f k8s/monitoring/servicemonitor.yaml
```

### 7.3 Set Up Alerting Rules

See `docs/MONITORING.md` for detailed alerting configuration.

---

## Step 8: Backup Configuration

### 8.1 Set Up Automated Backups

```bash
# Create backup cron job
kubectl apply -f k8s/backup-cronjob.yaml

# Verify backup job
kubectl get cronjobs -n research-ops
```

See `docs/DISASTER_RECOVERY.md` for backup procedures.

---

## Step 9: Security Hardening

### 9.1 Network Policies

```yaml
# k8s/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: research-ops-netpol
  namespace: research-ops
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: qdrant
      ports:
        - protocol: TCP
          port: 6333
```

Apply:
```bash
kubectl apply -f k8s/network-policy.yaml
```

### 9.2 Pod Security Standards

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: research-ops
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

---

## Troubleshooting

### Common Issues

#### 1. Pods Not Starting
```bash
# Check pod events
kubectl describe pod <pod-name> -n research-ops

# Check logs
kubectl logs <pod-name> -n research-ops

# Check resource quotas
kubectl describe quota -n research-ops
```

#### 2. Services Not Connecting
```bash
# Verify service endpoints
kubectl get endpoints -n research-ops

# Test connectivity from pod
kubectl exec -it <pod-name> -n research-ops -- \
  curl http://service-name.research-ops.svc.cluster.local:port
```

#### 3. Circuit Breaker Opening
```bash
# Check circuit breaker state
kubectl exec -it deployment/agent-orchestrator -n research-ops -- \
  curl http://localhost:8080/admin/circuit-breaker-status

# Check NIM health
kubectl exec -it deployment/reasoning-nim -n research-ops -- \
  curl http://localhost:8000/health
```

---

## Production Checklist

- [ ] EKS cluster created and configured
- [ ] All Docker images built and pushed to ECR
- [ ] Secrets configured and applied
- [ ] All services deployed and healthy
- [ ] Ingress configured with SSL certificates
- [ ] DNS records updated
- [ ] Integration tests passing
- [ ] Monitoring and alerting configured
- [ ] Backup automation enabled
- [ ] Network policies applied
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] On-call rotation configured

---

## Maintenance Windows

### Recommended Schedule
- **Weekly**: Review logs and metrics
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Full system review and optimization

### Update Procedure
1. Build new images with updated code
2. Push to ECR
3. Update deployment manifests
4. Apply changes: `kubectl apply -f k8s/`
5. Verify rollout: `kubectl rollout status deployment/<name> -n research-ops`
6. Rollback if needed: `kubectl rollout undo deployment/<name> -n research-ops`

---

## Support

For issues or questions:
- **Documentation**: `/docs/`
- **Slack**: #research-ops-deployment
- **Issues**: GitHub Issues

---

**Next Steps**:
1. Complete security audit
2. Set up monitoring dashboards
3. Configure automated backups
4. Schedule regular maintenance windows


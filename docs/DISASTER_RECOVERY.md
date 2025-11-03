# Disaster Recovery Plan for ResearchOps Agent

**Last Updated**: 2025-01-27  
**Version**: 1.0  
**Status**: Production Ready

---

## Overview

This document outlines the disaster recovery (DR) procedures for the ResearchOps Agent system. It covers backup strategies, recovery procedures, and business continuity planning.

---

## Recovery Objectives

### Recovery Time Objective (RTO)
**Target**: 15 minutes  
**Definition**: Maximum acceptable downtime before system must be operational

### Recovery Point Objective (RPO)
**Target**: 1 hour  
**Definition**: Maximum acceptable data loss (1 hour of synthesis cache/embeddings)

---

## Critical Components

### 1. Vector Database (Qdrant)
**Criticality**: HIGH  
**Data Type**: Paper embeddings, search indices  
**Impact**: Loss means re-indexing all papers

### 2. Synthesis Cache (Redis)
**Criticality**: MEDIUM  
**Data Type**: Cached synthesis results  
**Impact**: Performance degradation, re-computation required

### 3. Configuration & Secrets (Kubernetes Secrets)
**Criticality**: HIGH  
**Data Type**: API keys, NIM URLs, authentication tokens  
**Impact**: System cannot start without proper configuration

### 4. Application State (Pod logs, metrics)
**Criticality**: LOW  
**Data Type**: Runtime logs, metrics history  
**Impact**: Loss of historical data, debugging capability

---

## Backup Strategy

### 1. Vector Database Backups

#### Backup Schedule
- **Frequency**: Daily at 2:00 AM UTC
- **Retention**: 30 days
- **Location**: S3 bucket `research-ops-backups/qdrant/`
- **Format**: Qdrant snapshot (compressed)

#### Backup Procedure
```bash
#!/bin/bash
# Backup Qdrant vector database
# Run in Kubernetes cron job

# Create snapshot
kubectl exec -n research-ops qdrant-0 -- \
  curl -X POST "http://localhost:6333/snapshots/create"

# Wait for snapshot completion
SNAPSHOT_NAME=$(kubectl exec -n research-ops qdrant-0 -- \
  ls -t /qdrant/snapshots | head -1)

# Copy to S3
kubectl cp research-ops/qdrant-0:/qdrant/snapshots/$SNAPSHOT_NAME \
  /tmp/qdrant-snapshot

aws s3 cp /tmp/qdrant-snapshot \
  s3://research-ops-backups/qdrant/$(date +%Y%m%d)-snapshot.tar.gz

# Verify backup
aws s3 ls s3://research-ops-backups/qdrant/ --recursive --human-readable
```

#### Backup Verification
```bash
# Weekly backup verification
# Restore test snapshot and validate embedding count
kubectl exec -n research-ops qdrant-0 -- \
  curl -X GET "http://localhost:6333/collections/papers" | \
  jq '.result.vectors_count'
```

### 2. Synthesis Cache Backups

#### Backup Schedule
- **Frequency**: Hourly (during peak hours), Daily (off-peak)
- **Retention**: 7 days
- **Location**: S3 bucket `research-ops-backups/redis/`
- **Format**: Redis RDB dump

#### Backup Procedure
```bash
#!/bin/bash
# Backup Redis cache
# Run in Kubernetes cron job

# Trigger Redis backup (BGSAVE)
kubectl exec -n research-ops redis-0 -- redis-cli BGSAVE

# Wait for completion
while kubectl exec -n research-ops redis-0 -- redis-cli LASTSAVE | \
      diff - <(date +%s) > /dev/null; do
  sleep 1
done

# Copy RDB file to S3
kubectl cp research-ops/redis-0:/data/dump.rdb /tmp/redis-dump.rdb

aws s3 cp /tmp/redis-dump.rdb \
  s3://research-ops-backups/redis/$(date +%Y%m%d-%H%M)-dump.rdb
```

### 3. Configuration Backups

#### Backup Schedule
- **Frequency**: On every configuration change
- **Retention**: 90 days
- **Location**: S3 bucket `research-ops-backups/config/` (encrypted)

#### Backup Procedure
```bash
#!/bin/bash
# Backup Kubernetes secrets and configmaps

# Backup all secrets
kubectl get secrets -n research-ops -o yaml | \
  kubectl seal | \
  gzip > /tmp/secrets-$(date +%Y%m%d).yaml.gz

aws s3 cp /tmp/secrets-$(date +%Y%m%d).yaml.gz \
  s3://research-ops-backups/config/secrets/

# Backup configmaps
kubectl get configmaps -n research-ops -o yaml | \
  gzip > /tmp/configmaps-$(date +%Y%m%d).yaml.gz

aws s3 cp /tmp/configmaps-$(date +%Y%m%d).yaml.gz \
  s3://research-ops-backups/config/configmaps/
```

---

## Disaster Recovery Procedures

### Scenario 1: Vector Database Failure

#### Detection
- Monitoring alerts: Qdrant pod crash loops
- Health check failures: `/health` endpoint returns 503
- User reports: Search functionality not working

#### Recovery Steps

1. **Assess Damage**
   ```bash
   # Check Qdrant pod status
   kubectl get pods -n research-ops | grep qdrant
   
   # Check persistent volume
   kubectl describe pvc qdrant-data -n research-ops
   ```

2. **Restore from Backup**
   ```bash
   # List available backups
   aws s3 ls s3://research-ops-backups/qdrant/ --recursive | \
     sort -r | head -5
   
   # Download latest backup
   LATEST_BACKUP=$(aws s3 ls s3://research-ops-backups/qdrant/ | \
     sort -r | head -1 | awk '{print $4}')
   
   aws s3 cp s3://research-ops-backups/qdrant/$LATEST_BACKUP \
     /tmp/qdrant-restore.tar.gz
   
   # Extract and restore
   tar -xzf /tmp/qdrant-restore.tar.gz -C /tmp/qdrant-restore
   
   # Copy to new Qdrant instance
   kubectl cp /tmp/qdrant-restore research-ops/qdrant-0:/qdrant/snapshots/
   
   # Restore snapshot
   kubectl exec -n research-ops qdrant-0 -- \
     curl -X POST "http://localhost:6333/snapshots/upload" \
     -F "file=@/qdrant/snapshots/$(basename $LATEST_BACKUP .tar.gz)"
   ```

3. **Validate Restoration**
   ```bash
   # Verify embedding count
   kubectl exec -n research-ops qdrant-0 -- \
     curl -X GET "http://localhost:6333/collections/papers" | \
     jq '.result.vectors_count'
   
   # Run smoke tests
   curl -X POST http://api.research-ops.svc.cluster.local/research \
     -H "Content-Type: application/json" \
     -d '{"query": "machine learning", "max_papers": 1}'
   ```

4. **Update Service Endpoints** (if new instance)
   ```bash
   # Update service if Qdrant was recreated
   kubectl apply -f k8s/vector-db-deployment.yaml
   ```

**Estimated Recovery Time**: 10-15 minutes

---

### Scenario 2: Complete Cluster Failure

#### Detection
- All pods unreachable
- Kubernetes API server down
- Cloud provider alerts

#### Recovery Steps

1. **Provision New Infrastructure**
   ```bash
   # Deploy new EKS cluster (or use existing backup cluster)
   eksctl create cluster --name research-ops-dr --region us-east-1
   
   # Configure kubectl
   aws eks update-kubeconfig --name research-ops-dr --region us-east-1
   ```

2. **Restore Namespace and RBAC**
   ```bash
   # Apply namespace
   kubectl apply -f k8s/namespace.yaml
   
   # Restore secrets from backup
   aws s3 cp s3://research-ops-backups/config/secrets/secrets-latest.yaml.gz \
     /tmp/secrets.yaml.gz
   
   gunzip /tmp/secrets.yaml.gz
   kubectl apply -f /tmp/secrets.yaml
   ```

3. **Restore Vector Database**
   - Follow Scenario 1 steps 2-4

4. **Deploy All Services**
   ```bash
   # Deploy in order of dependencies
   kubectl apply -f k8s/vector-db-deployment.yaml
   kubectl apply -f k8s/reasoning-nim-deployment.yaml
   kubectl apply -f k8s/embedding-nim-deployment.yaml
   kubectl apply -f k8s/agent-orchestrator-deployment.yaml
   kubectl apply -f k8s/web-ui-deployment.yaml
   kubectl apply -f k8s/ingress.yaml
   ```

5. **Validate All Services**
   ```bash
   # Check all pods are running
   kubectl get pods -n research-ops
   
   # Run integration tests
   python src/test_comprehensive_integration.py
   
   # Test API endpoints
   curl http://api.research-ops.svc.cluster.local/health
   ```

**Estimated Recovery Time**: 30-45 minutes (with pre-provisioned cluster: 15 minutes)

---

### Scenario 3: Data Corruption (Partial)

#### Detection
- Search results inconsistent
- Embeddings failing validation
- User reports incorrect results

#### Recovery Steps

1. **Identify Corrupted Data**
   ```bash
   # Run data validation script
   python scripts/validate_qdrant_data.py
   ```

2. **Restore Affected Collections**
   ```bash
   # Restore specific collection from backup
   COLLECTION_NAME="papers"
   BACKUP_DATE="20250126"
   
   aws s3 cp \
     s3://research-ops-backups/qdrant/$BACKUP_DATE-snapshot.tar.gz \
     /tmp/
   
   # Extract and restore only affected collection
   # (Implementation depends on Qdrant snapshot format)
   ```

3. **Re-index if Necessary**
   ```bash
   # Trigger re-indexing of affected papers
   curl -X POST http://api.research-ops.svc.cluster.local/admin/reindex \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{"collection": "papers", "paper_ids": ["id1", "id2"]}'
   ```

**Estimated Recovery Time**: 5-10 minutes (partial), 15-20 minutes (full re-index)

---

## Backup Monitoring and Alerting

### Backup Success Monitoring
```yaml
# Prometheus alert rule
groups:
  - name: backup_alerts
    rules:
      - alert: BackupFailed
        expr: backup_last_success_time < (now() - 86400)
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "Backup has not completed in 24 hours"
          description: "Last successful backup was {{ $value }} seconds ago"
      
      - alert: BackupSizeAnomaly
        expr: abs(backup_size_bytes / backup_size_bytes offset 1d - 1) > 0.2
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Backup size changed significantly"
```

### Backup Verification Jobs
```yaml
# Kubernetes CronJob for backup verification
apiVersion: batch/v1
kind: CronJob
metadata:
  name: verify-backups
  namespace: research-ops
spec:
  schedule: "0 3 * * 0"  # Weekly on Sunday at 3 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: verify
            image: research-ops/backup-verifier:latest
            command:
              - /bin/bash
              - -c
              - |
                # Verify Qdrant backup integrity
                aws s3 ls s3://research-ops-backups/qdrant/ | \
                  tail -1 | \
                  xargs -I {} aws s3 cp s3://research-ops-backups/qdrant/{} /tmp/verify.tar.gz
                
                # Extract and verify
                tar -tzf /tmp/verify.tar.gz > /dev/null && echo "Backup valid" || exit 1
          restartPolicy: OnFailure
```

---

## Disaster Recovery Testing

### Test Schedule
- **Monthly**: Partial recovery test (single component)
- **Quarterly**: Full cluster failure simulation
- **Annually**: Complete DR drill with stakeholders

### Test Procedure
1. Create isolated test environment
2. Restore from most recent backup
3. Validate all services operational
4. Run comprehensive integration tests
5. Document any issues and update procedures

### Success Criteria
- All services operational within RTO (15 minutes)
- Data loss within RPO (1 hour)
- All integration tests pass
- No manual intervention required beyond documented procedures

---

## Backup Storage Costs

### Estimated Monthly Costs (AWS S3)
- **Qdrant snapshots**: ~50 GB × $0.023/GB = $1.15/month
- **Redis dumps**: ~5 GB × $0.023/GB = $0.12/month
- **Configuration backups**: ~1 GB × $0.023/GB = $0.02/month
- **Total**: ~$1.30/month

### Cost Optimization
- Enable S3 lifecycle policies for older backups
- Compress backups before upload
- Use S3 Intelligent-Tiering for infrequently accessed backups

---

## Contact Information

### On-Call Rotation
- **Primary**: DevOps Team Lead
- **Secondary**: Platform Engineer
- **Escalation**: Engineering Manager

### Emergency Contacts
- **Slack**: #research-ops-incidents
- **PagerDuty**: ResearchOps On-Call
- **Email**: incidents@research-ops.example.com

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-01-27 | 1.0 | Initial disaster recovery plan | Platform Team |

---

**Next Steps**: 
1. Implement backup automation scripts
2. Set up monitoring and alerting
3. Schedule first DR test
4. Document lessons learned and update procedures


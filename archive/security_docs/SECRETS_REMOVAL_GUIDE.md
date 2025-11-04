# Secrets Removal Guide

## Critical Security Issue: Exposed Secrets in Git

The file `k8s/secrets.yaml` contains sensitive credentials that were committed to version control:
- NGC API Key
- AWS Access Key ID
- AWS Secret Access Key

## Immediate Actions Required

### Step 1: Remove from Git History

**⚠️ WARNING**: This rewrites git history. Coordinate with your team before proceeding.

```bash
# Option A: Use git-filter-repo (recommended)
pip install git-filter-repo
git filter-repo --path k8s/secrets.yaml --invert-paths

# Option B: Use BFG Repo-Cleaner (alternative)
# Download from https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files k8s/secrets.yaml
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Step 2: Rotate All Exposed Credentials

**CRITICAL**: All exposed credentials must be rotated immediately:

1. **NGC API Key**:
   - Go to https://ngc.nvidia.com
   - Navigate to Account → API Keys
   - Delete the exposed key
   - Create a new API key
   - Update Kubernetes secret with new key

2. **AWS Credentials**:
   - Go to AWS IAM Console
   - Delete the exposed access key
   - Create new access key pair
   - Update Kubernetes secret with new credentials

### Step 3: Update Kubernetes Secrets

```bash
# Delete existing secret
kubectl delete secret nvidia-ngc-secret -n research-ops
kubectl delete secret aws-credentials -n research-ops

# Create new secrets with rotated credentials
kubectl create secret generic nvidia-ngc-secret \
  --from-literal=NGC_API_KEY=<NEW_NGC_KEY> \
  -n research-ops

kubectl create secret generic aws-credentials \
  --from-literal=AWS_ACCESS_KEY_ID=<NEW_ACCESS_KEY> \
  --from-literal=AWS_SECRET_ACCESS_KEY=<NEW_SECRET_KEY> \
  --from-literal=AWS_DEFAULT_REGION=us-east-2 \
  -n research-ops
```

### Step 4: Verify .gitignore

The file `k8s/secrets.yaml` is already in `.gitignore`. Verify it's there:

```bash
grep -q "k8s/secrets.yaml" .gitignore && echo "✅ Already in .gitignore" || echo "❌ Not in .gitignore"
```

### Step 5: Create Secrets Template

Create a template file for future reference:

```bash
cat > k8s/secrets.yaml.template << 'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: nvidia-ngc-secret
  namespace: research-ops
type: Opaque
stringData:
  NGC_API_KEY: "<REPLACE_WITH_NGC_API_KEY>"
---
apiVersion: v1
kind: Secret
metadata:
  name: aws-credentials
  namespace: research-ops
type: Opaque
stringData:
  AWS_ACCESS_KEY_ID: "<REPLACE_WITH_AWS_ACCESS_KEY_ID>"
  AWS_SECRET_ACCESS_KEY: "<REPLACE_WITH_AWS_SECRET_ACCESS_KEY>"
  AWS_DEFAULT_REGION: "us-east-2"
EOF
```

### Step 6: Force Push (if using git-filter-repo)

**⚠️ WARNING**: This will rewrite remote history. Only do this if:
1. You're the only one working on this repository, OR
2. You've coordinated with all team members

```bash
git push origin --force --all
git push origin --force --tags
```

## Prevention

1. **Never commit secrets to Git** - Always use `.gitignore`
2. **Use Kubernetes Secrets** - Store secrets in K8s, not in code
3. **Use AWS Secrets Manager** - For production, migrate to AWS Secrets Manager
4. **Pre-commit hooks** - Add git hooks to scan for secrets before commit

## Post-Remediation Checklist

- [ ] Secrets removed from Git history
- [ ] All credentials rotated
- [ ] New secrets created in Kubernetes
- [ ] `.gitignore` verified
- [ ] Secrets template created
- [ ] Team notified of credential rotation
- [ ] Security audit completed

## Estimated Cost Exposure

Based on the exposed credentials:
- **NGC API Key**: Potential $50K/year in unauthorized usage
- **AWS Credentials**: Potential $20K/month in compute costs ($240K/year when annualized)
- **Total Estimated Exposure**: $290K/year (NGC $50K/year + AWS $240K/year)

**Action Required**: Rotate credentials within 24 hours.


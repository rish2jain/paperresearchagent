# 🔐 AWS Access Key & Secret Setup Guide

This guide walks you through creating and configuring AWS access keys for your research-ops-agent project.

---

## Option 1: Extract Existing Credentials (Quick)

If you already have AWS credentials configured and want to use them:

### Step 1: View Your Credentials

```bash
# View the Access Key ID (last 4 characters are visible in aws configure list)
aws configure list

# View the full credentials (CAUTION: Secrets will be visible)
cat ~/.aws/credentials
```

**Note:** The credentials file will show your access key and secret in plain text.

### Step 2: Update secrets.yaml

Once you have your credentials, update the `k8s/secrets.yaml` file:

```bash
nano k8s/secrets.yaml
# Or use your preferred editor
```

Update these values:
- `AWS_ACCESS_KEY_ID`: Your Access Key ID
- `AWS_SECRET_ACCESS_KEY`: Your Secret Access Key
- `AWS_DEFAULT_REGION`: us-east-1 (already set)

---

## Option 2: Create IAM User with Specific Permissions (Recommended)

For better security, create a dedicated IAM user with only the permissions needed for this project.

### Step 1: Create IAM User via AWS Console

1. **Go to AWS IAM Console**
   - Navigate to: https://console.aws.amazon.com/iam/
   - Or search for "IAM" in AWS Console

2. **Create New User**
   - Click "Users" in the left sidebar
   - Click "Create user"
   - Enter username: `research-ops-agent` (or your preferred name)
   - Click "Next"

3. **Attach Policies**
   - Select "Attach policies directly"
   - Attach these policies:
     - `AmazonEKSClusterPolicy`
     - `AmazonEKSWorkerNodePolicy`
     - `AmazonEC2FullAccess` (for EKS node management)
     - `AmazonElasticContainerRegistryPublicFullAccess` (if using ECR)
   - Click "Next"

4. **Review and Create**
   - Review the settings
   - Click "Create user"

### Step 2: Create Access Keys

1. **Select the User**
   - Click on the newly created user
   - Go to the "Security credentials" tab

2. **Create Access Key**
   - Scroll to "Access keys"
   - Click "Create access key"
   - Select use case: "Application running outside AWS"
   - Click "Next"
   - Add a description (optional): "Research Ops Agent - EKS Deployment"
   - Click "Create access key"

3. **Save Credentials**
   - **IMPORTANT**: Copy both the Access Key ID and Secret Access Key
   - Store them securely (you won't be able to see the secret again!)
   - Download the CSV file or copy them manually

### Step 3: Configure AWS CLI with New Credentials

```bash
# Configure AWS CLI with the new IAM user credentials
aws configure

# You'll be prompted for:
# AWS Access Key ID: [Paste your Access Key ID]
# AWS Secret Access Key: [Paste your Secret Access Key]
# Default region name: us-east-1
# Default output format: json

# Verify the configuration
aws sts get-caller-identity
```

You should see your IAM user ARN instead of root account.

### Step 4: Update secrets.yaml

```bash
# Edit the secrets file
nano k8s/secrets.yaml
```

Update with your new credentials:
```yaml
AWS_ACCESS_KEY_ID: "YOUR_ACCESS_KEY_ID_HERE"
AWS_SECRET_ACCESS_KEY: "YOUR_SECRET_ACCESS_KEY_HERE"
AWS_DEFAULT_REGION: "us-east-1"
```

---

## Option 3: Use AWS CLI to Extract Credentials Programmatically

If you have the AWS CLI configured and want to extract credentials:

```bash
# View Access Key ID
aws configure get aws_access_key_id

# Note: Secret key cannot be retrieved via CLI (security feature)
# You'll need to check ~/.aws/credentials or create a new access key
```

---

## Verification Steps

### 1. Verify AWS CLI Configuration

```bash
# Check your AWS identity
aws sts get-caller-identity

# Should return your account/user info
```

### 2. Verify EKS Access

```bash
# List EKS clusters (if any exist)
aws eks list-clusters --region us-east-1
```

### 3. Verify secrets.yaml is Configured

```bash
# Check that secrets.yaml exists and is not using placeholders
grep -E "(YOUR_AWS|PLACEHOLDER)" k8s/secrets.yaml || echo "✅ No placeholders found"
```

---

## Security Best Practices

1. **Never commit secrets.yaml to git**
   - It's already in `.gitignore`
   - Double-check before committing: `git status`

2. **Use IAM users instead of root account**
   - Root credentials have full access - security risk!
   - IAM users can have limited, specific permissions

3. **Rotate access keys regularly**
   - AWS recommends rotating keys every 90 days
   - Create new key → Update config → Delete old key

4. **Use AWS Secrets Manager for production**
   - For production deployments, consider using AWS Secrets Manager
   - Store credentials securely in AWS instead of local files

---

## Troubleshooting

### Error: "Unable to locate credentials"

```bash
# Re-configure AWS CLI
aws configure
```

### Error: "Access Denied" when running AWS commands

- Check that your IAM user has the necessary permissions
- Verify the access key is still active (not deleted)
- Check if there are any IAM policy restrictions

### Error: "Invalid Access Key ID"

- Verify you copied the Access Key ID correctly
- Check for extra spaces or special characters
- Make sure you're using the right credentials file/profile

---

## Next Steps

After configuring AWS credentials:

1. ✅ Verify AWS CLI: `aws sts get-caller-identity`
2. ✅ Update `k8s/secrets.yaml` with your credentials
3. ✅ Verify secrets file: `grep -i "your_aws" k8s/secrets.yaml`
4. ✅ Proceed with EKS deployment as per `HACKATHON_SETUP_GUIDE.md`

---

## Quick Reference

| What | Where |
|------|-------|
| AWS Console | https://console.aws.amazon.com/ |
| IAM Console | https://console.aws.amazon.com/iam/ |
| AWS CLI Config | `~/.aws/config` |
| AWS Credentials | `~/.aws/credentials` |
| Project Secrets | `k8s/secrets.yaml` |


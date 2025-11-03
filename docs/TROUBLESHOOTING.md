# Troubleshooting Guide

This guide helps you diagnose and fix common issues with ResearchOps Agent.

## Table of Contents

- [NIM Connectivity Issues](#nim-connectivity-issues)
- [Agent Workflow Problems](#agent-workflow-problems)
- [Kubernetes Deployment Issues](#kubernetes-deployment-issues)
- [Performance Problems](#performance-problems)
- [Configuration Issues](#configuration-issues)
- [API Errors](#api-errors)

---

## NIM Connectivity Issues

### Problem: Reasoning NIM not responding

**Symptoms:**
- API health check shows `reasoning_nim: false`
- Timeout errors in logs
- Agent workflow fails at analysis step

**Solutions:**

1. **Check NIM pod status:**
```bash
kubectl get pods -n research-ops | grep reasoning-nim
```

2. **Check NIM logs:**
```bash
kubectl logs -n research-ops deployment/reasoning-nim
```

3. **Verify NIM is accessible:**
```bash
kubectl exec -n research-ops deployment/agent-orchestrator -- \
  curl -v http://reasoning-nim:8000/v1/health/live
```

4. **Common issues:**
   - **Pod not running**: Check GPU availability, resource limits
   - **Image pull errors**: Verify NGC_API_KEY in secrets
   - **Port conflicts**: Ensure port 8000 is not in use

### Problem: Embedding NIM not responding

**Symptoms:**
- Similar to Reasoning NIM issues
- Scout agent fails to find papers
- Embedding generation errors

**Solutions:**

1. **Check embedding NIM:**
```bash
kubectl get pods -n research-ops | grep embedding-nim
kubectl logs -n research-ops deployment/embedding-nim
```

2. **Test connectivity:**
```bash
kubectl exec -n research-ops deployment/agent-orchestrator -- \
  curl -v http://embedding-nim:8001/v1/health/live
```

---

## Agent Workflow Problems

### Problem: No papers found

**Symptoms:**
- `papers_analyzed: 0` in results
- Scout agent logs show no results

**Solutions:**

1. **Check arXiv/PubMed connectivity:**
   - Verify network access from cluster
   - Check if external APIs are blocked by firewall

2. **Verify search query:**
   - Query may be too specific
   - Try a broader search term

3. **Check relevance threshold:**
```bash
# Lower threshold if too restrictive
export RELEVANCE_THRESHOLD=0.5
```

### Problem: Synthesis quality is low

**Symptoms:**
- Synthesis refinement loops many times
- Quality scores consistently below threshold

**Solutions:**

1. **Increase paper count:**
   - More papers provide better coverage
   - Set `max_papers` to 20-30

2. **Adjust quality threshold:**
```bash
export SYNTHESIS_QUALITY_THRESHOLD=0.7  # Lower threshold
```

3. **Check paper relevance:**
   - Ensure papers are actually relevant to query
   - Review Scout agent filtering decisions

### Problem: Agent decisions not appearing

**Symptoms:**
- `decisions` array empty in API response
- No decision logs in console

**Solutions:**

1. **Check decision logging:**
   - Verify DecisionLog class is initialized
   - Check that agents call `log_decision()`

2. **Review agent code:**
   - Ensure all autonomous decisions are logged
   - Check console output for decision messages

---

## Kubernetes Deployment Issues

### Problem: Pods stuck in Pending

**Symptoms:**
```bash
kubectl get pods
# NAME                           READY   STATUS    RESTARTS   AGE
# reasoning-nim-xxx              0/1     Pending   0          5m
```

**Solutions:**

1. **Check resource availability:**
```bash
kubectl describe pod -n research-ops reasoning-nim-xxx
```

2. **Common causes:**
   - **Insufficient GPU**: Ensure GPU nodes are available
   - **Resource limits**: Check CPU/memory availability
   - **Node selector**: Verify node labels match selector

3. **Fix GPU node issues:**
```bash
# Check GPU nodes
kubectl get nodes -l accelerator=nvidia-tesla-t4

# Install NVIDIA device plugin if missing
kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.13.0/nvidia-device-plugin.yml
```

### Problem: Image pull errors

**Symptoms:**
```bash
# Pod events show:
# Error: ImagePullBackOff
# Failed to pull image "nvcr.io/..."
```

**Solutions:**

1. **Verify NGC secret:**
```bash
kubectl get secret nvidia-ngc-secret -n research-ops
```

2. **Check API key:**
   - Get NGC API key from https://ngc.nvidia.com/setup/api-key
   - Verify key has pull permissions

3. **Create/update secret:**
```bash
kubectl create secret docker-registry ngc-secret \
  --docker-server=nvcr.io \
  --docker-username='$oauthtoken' \
  --docker-password=YOUR_NGC_API_KEY \
  --namespace=research-ops
```

### Problem: Services not accessible

**Symptoms:**
- Cannot connect to API from outside cluster
- Port forwarding works but LoadBalancer doesn't

**Solutions:**

1. **Check service type:**
```bash
kubectl get svc -n research-ops
# Should show ClusterIP (not LoadBalancer)
```

2. **Use Ingress instead:**
```bash
# Deploy ingress
kubectl apply -f k8s/ingress.yaml

# Get ingress URL
kubectl get ingress -n research-ops
```

3. **Use port-forward for testing:**
```bash
kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080
```

---

## Performance Problems

### Problem: Slow synthesis (takes > 5 minutes)

**Symptoms:**
- Requests timeout
- High CPU/memory usage

**Solutions:**

1. **Reduce paper count:**
```bash
# Set smaller max_papers
export MAX_PAPERS_PER_SEARCH=10
```

2. **Check resource limits:**
```bash
kubectl top pods -n research-ops
kubectl describe pod -n research-ops agent-orchestrator-xxx
```

3. **Optimize clustering:**
```bash
# Reduce clustering complexity
export CLUSTERING_MIN_SAMPLES=2
export CLUSTERING_EPS=0.4
```

4. **Increase synthesis iterations limit:**
```bash
export SYNTHESIS_MAX_ITERATIONS=1  # Reduce refinement cycles
```

### Problem: High memory usage

**Symptoms:**
- Pods get OOMKilled
- Memory usage near limits

**Solutions:**

1. **Check memory limits:**
```bash
kubectl describe deployment -n research-ops agent-orchestrator
```

2. **Reduce batch sizes:**
   - Embed fewer papers at once
   - Process papers sequentially instead of in parallel

3. **Enable embedding cache:**
   - Caching reduces redundant API calls
   - Already enabled by default

---

## Configuration Issues

### Problem: Environment variables not working

**Symptoms:**
- Config changes don't take effect
- Default values always used

**Solutions:**

1. **Verify environment variables:**
```bash
kubectl exec -n research-ops deployment/agent-orchestrator -- env | grep RELEVANCE
```

2. **Update deployment:**
```bash
# Edit deployment
kubectl edit deployment agent-orchestrator -n research-ops

# Add or update env vars in container spec
```

3. **Redeploy:**
```bash
kubectl rollout restart deployment/agent-orchestrator -n research-ops
```

### Problem: Invalid configuration values

**Symptoms:**
- Validation errors in logs
- Agent refuses to start

**Solutions:**

1. **Check configuration validation:**
```python
from src.config import get_config
config = get_config()
config.validate()  # Will show errors
```

2. **Common issues:**
   - Thresholds outside [0, 1] range
   - URLs not starting with http:// or https://
   - Negative integer values

3. **Fix in environment:**
```bash
# Correct format
export RELEVANCE_THRESHOLD=0.7
export REASONING_NIM_URL=http://reasoning-nim:8000
```

---

## API Errors

### Problem: 400 Bad Request

**Symptoms:**
```json
{
  "error": "Invalid input",
  "message": "Query contains invalid pattern: <script>"
}
```

**Solutions:**

1. **Input validation:**
   - Query contains blocked patterns (XSS protection)
   - Query too long (> 500 chars) or too short (< 1 char)
   - max_papers outside valid range (1-50)

2. **Fix query:**
   - Remove script tags and special characters
   - Keep query to reasonable length
   - Use valid max_papers value

### Problem: 500 Internal Server Error

**Symptoms:**
```json
{
  "error": "Internal error",
  "message": "..."
}
```

**Solutions:**

1. **Check logs:**
```bash
kubectl logs -n research-ops deployment/agent-orchestrator --tail=100
```

2. **Common causes:**
   - NIM connection failure (check health endpoint)
   - Network timeout (increase timeout values)
   - Resource exhaustion (check pod resources)

3. **Retry:**
   - API uses retry logic, but persistent failures indicate deeper issues
   - Check NIM availability first

### Problem: Timeout errors

**Symptoms:**
- Requests take > 5 minutes
- Client receives timeout

**Solutions:**

1. **Increase timeout:**
```bash
# In API config
export REQUEST_TIMEOUT=600  # 10 minutes
```

2. **Reduce workload:**
   - Lower max_papers
   - Simplify query
   - Reduce synthesis iterations

3. **Check network:**
   - Slow connections between services
   - Check cluster network performance

---

## Diagnostic Commands

### Quick Health Check
```bash
# Check all pods
kubectl get pods -n research-ops

# Check service endpoints
kubectl get svc -n research-ops

# Test API health
curl http://localhost:8080/health
```

### Log Analysis
```bash
# Recent logs from orchestrator
kubectl logs -n research-ops deployment/agent-orchestrator --tail=50

# Follow logs in real-time
kubectl logs -f -n research-ops deployment/agent-orchestrator

# Check for errors
kubectl logs -n research-ops deployment/agent-orchestrator | grep -i error
```

### Resource Monitoring
```bash
# Pod resource usage
kubectl top pods -n research-ops

# Node resource usage
kubectl top nodes

# Detailed pod info
kubectl describe pod -n research-ops <pod-name>
```

---

## Getting Help

If issues persist:

1. **Collect diagnostic information:**
```bash
# Save logs
kubectl logs -n research-ops deployment/agent-orchestrator > orchestrator.log
kubectl logs -n research-ops deployment/reasoning-nim > reasoning-nim.log
kubectl logs -n research-ops deployment/embedding-nim > embedding-nim.log

# Save pod descriptions
kubectl describe pods -n research-ops > pods-description.txt
```

2. **Check GitHub Issues:**
   - Search for similar issues
   - Create new issue with diagnostic info

3. **Review Documentation:**
   - [README.md](../README.md)
   - [DEPLOYMENT.md](../DEPLOYMENT.md)
   - [Architecture Diagrams](Architecture_Diagrams.md)

---

**Last Updated:** 2025-01-01


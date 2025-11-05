# Reasoning NIM OOM Issue - Documentation

**Date:** 2025-11-05  
**Status:** Known Limitation  
**Severity:** High - Blocks Reasoning NIM deployment

## Problem

The Reasoning NIM pod (`nvidia/llama-3.1-nemotron-nano-8b-v1:1.8.4`) repeatedly fails with OOMKilled (Exit Code 137) during TensorRT engine compilation, even with maximum memory allocation.

## Symptoms

- Pod restarts every ~13 minutes during TensorRT compilation
- Exit Code: 137 (OOMKilled)
- Memory limit: 29Gi (maximum safe limit for node)
- Node allocatable: ~30GB total
- Pattern: Fails consistently during TensorRT compilation phase

## Root Cause

TensorRT engine compilation for the 8B Llama model requires **>29Gi memory** during peak compilation phases, exceeding the available capacity on g5.2xlarge nodes (which have ~30GB allocatable memory).

### Attempted Fixes

1. **Memory Limit Increases:**
   - Initial: 20Gi → OOM at ~13 min
   - First increase: 28Gi → OOM at ~13 min  
   - Maximum: 29Gi → OOM at ~13 min

2. **Cache Configuration:**
   - PVC is bound and configured (`/opt/nim/.cache`)
   - Cache may not persist if compilation fails before completion

## Technical Details

### Node Specifications
- **Instance Type:** g5.2xlarge
- **Allocatable Memory:** ~30GB (31,482,280Ki)
- **GPU:** NVIDIA A10G (24GB)
- **vCPU:** 7.91 allocatable

### Memory Configuration
```yaml
resources:
  requests:
    memory: "20Gi"
  limits:
    memory: "29Gi"  # Maximum safe limit (leaves ~1GB for system)
```

### Build Timeline (Failed Attempts)
- Checkpoint conversion: ~11 seconds (or 0.41s if cached)
- TensorRT compilation: Fails at ~13 minutes
- Expected total: ~15-20 minutes (never reached)

## Solutions

### Option 1: Use Larger Node Instance (Recommended)
Switch to **g5.4xlarge** which has 64GB RAM:

```yaml
nodeSelector:
  node.kubernetes.io/instance-type: g5.4xlarge
```

**Pros:**
- Sufficient memory for TensorRT compilation
- No code changes required
- Reliable solution

**Cons:**
- Higher cost (~2x)
- Requires updating node group

### Option 2: Use Pre-built Engine Cache
If the TensorRT engine can be pre-built and cached:

1. Build engine on a larger node
2. Export engine to PVC
3. Mount in deployment

**Status:** Needs investigation - cache path exists but may not persist engine files properly.

### Option 3: Use Smaller Model Variant
Consider using a smaller model that fits in memory:
- `llama-3.1-nemotron-nano-4b-v1` (if available)
- Other 4B or smaller variants

**Pros:**
- Fits in current infrastructure
- Lower memory requirements

**Cons:**
- Reduced model capability
- May not meet requirements

### Option 4: Disable TensorRT (Fallback)
Use vLLM backend instead of TensorRT:

```yaml
env:
  - name: NIM_ENGINE
    value: "vllm"  # Instead of tensorrt_llm
```

**Pros:**
- Lower memory requirements
- Still functional

**Cons:**
- Slower inference
- May not meet performance requirements

## Current Status

- **Deployment:** Failing with OOMKilled
- **Workaround:** None currently available
- **Action Required:** Choose solution above

## Recommendations

1. **Short-term:** Document this limitation for hackathon judges
2. **Medium-term:** Consider Option 1 (larger node) if budget allows
3. **Long-term:** Implement pre-built engine cache strategy

## Related Files

- `k8s/reasoning-nim-deployment.yaml` - Deployment configuration
- `k8s/reasoning-nim-cache-pvc.yaml` - Cache volume configuration
- `NEXT_STEPS_COMPLETED.md` - Previous troubleshooting attempts

## Notes

- Embedding NIM works fine with 8Gi limit (smaller model)
- This is specific to the 8B reasoning model
- TensorRT compilation is a one-time process (if it completes, subsequent starts are fast)

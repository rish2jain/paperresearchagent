# Get Your NGC API Key

This guide explains how to obtain and configure your NVIDIA NGC API key for ResearchOps Agent.

**Related:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#problem-ngc-api-key-issues-401403-errors) for fixing NGC key issues.

## Option 1: From NGC Website (Recommended)

1. **Go to NGC API Key page**:
   ```
   https://org.ngc.nvidia.com/setup/api-key
   ```

2. **Copy your existing key** OR **Generate new one**:
   - If you see an existing key, click "Show" and copy it
   - If generating new: Select **"Full Access"**

3. **Export the key**:
   ```bash
   export NGC_API_KEY='nvapi-YOUR-KEY-HERE'
   ```

4. **Test it**:
   ```bash
   curl -H "Authorization: Bearer $NGC_API_KEY" \
     https://api.ngc.nvidia.com/v2/org/nim/team/nvidia/models
   ```

   Should return JSON (not "Unauthorized")

5. **Run the update script**:
   ```bash
   ./scripts/update-ngc-key.sh
   ```

---

## What Changed (Good News!)

Your error changed from **403 → 401**:
- ✅ **403 Forbidden → 401 Unauthorized** = Licenses are being accepted!
- ❌ **401 Unauthorized** = Just need to export the right NGC key

This means the licenses are working or propagating. Once you export your NGC key, the update script should work!

---

## Quick Test

```bash
# 1. Export your NGC API key from the website
export NGC_API_KEY='nvapi-xxxxx-your-key-xxxxx'

# 2. Test it
curl -H "Authorization: Bearer $NGC_API_KEY" \
  https://api.ngc.nvidia.com/v2/org/nim/team/nvidia/models

# 3. If test shows JSON data, run:
./scripts/update-ngc-key.sh
```

---

**The 403→401 change is progress!** Once you export the right key, it should work.

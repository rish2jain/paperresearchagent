# ⚡ Quick Start Guide

**Last Updated:** 2025-01-15

**For the full detailed guide, see: [HACKATHON_SETUP_GUIDE.md](HACKATHON_SETUP_GUIDE.md)**

---

## 🚀 3-Day Timeline

### Day 1: Setup (2-3 hours)

```bash
# 1. AWS Account & CLI Setup (30 min)
# - Create AWS account
# - Install: awscli, eksctl, kubectl
# - Configure: aws configure
# - Request $100 hackathon credits

# 2. NGC Account Setup (15 min)
# - Sign up at: https://ngc.nvidia.com/
# - Get API key: https://ngc.nvidia.com/setup/api-key

# 3. Local Setup (30 min)
cd /Users/rish2jain/Documents/Hackathons/research-ops-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Test Locally (30 min)
python src/api.py  # Terminal 1
streamlit run src/web_ui.py  # Terminal 2
# Open: http://localhost:8501
```

### Day 2: Deployment (3-4 hours)

```bash
# 1. Prepare Secrets (15 min)
cp k8s/secrets.yaml.template k8s/secrets.yaml
nano k8s/secrets.yaml  # Fill in NGC_API_KEY and AWS credentials

# 2. Deploy to EKS (30-45 min)
cd k8s
export NGC_API_KEY="your_key_here"
chmod +x deploy.sh
./deploy.sh

# 3. Verify Deployment (15 min)
kubectl get pods -n research-ops
kubectl get svc -n research-ops
kubectl port-forward -n research-ops svc/web-ui 8501:8501
# Open: http://localhost:8501

# 4. Test End-to-End (30 min)
# - Test with multiple queries
# - Verify decision logging
# - Check all features work
```

### Day 3: Demo & Submission (2-3 hours)

```bash
# 1. Record Demo Video (60-90 min)
# - Use macOS Screen Recording or OBS
# - Follow script from README.md
# - Keep under 3 minutes!
# - Upload to YouTube

# 2. Make Repository Public (15 min)
# - Create GitHub repo
# - Push all code
# - Make public
# - Update README with links

# 3. Submit to Devpost (30 min)
# - Go to: https://nvidia-aws.devpost.com/
# - Create project
# - Fill all fields
# - Add video link
# - Submit before deadline!
```

---

## 📋 Essential Commands

### Local Testing
```bash
# API
python src/api.py
curl http://localhost:8080/health

# Web UI
streamlit run src/web_ui.py
# Open: http://localhost:8501
```

### EKS Deployment
```bash
# Deploy everything
cd k8s && ./deploy.sh

# Check status
kubectl get pods -n research-ops
kubectl logs -n research-ops deployment/agent-orchestrator

# Access services
kubectl port-forward -n research-ops svc/web-ui 8501:8501
kubectl port-forward -n research-ops svc/agent-orchestrator 8080:8080
```

### Testing
```bash
# Test API
curl -X POST http://localhost:8080/research \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "max_papers": 10}'

# Test health
curl http://localhost:8080/health
```

---

## ✅ Pre-Submission Checklist

- [ ] AWS account configured
- [ ] NGC API key obtained
- [ ] EKS cluster deployed
- [ ] All pods running
- [ ] Demo video recorded (under 3 min)
- [ ] Video uploaded to YouTube
- [ ] Repository public on GitHub
- [ ] README updated with links
- [ ] Devpost submission created
- [ ] **Submit before Nov 3, 2025 @ 2:00pm EST!**

---

## 🎯 Demo Video Script (Quick Version)

```
[0:00-0:30] Problem: Researcher with papers, 8+ hours of work
[0:30-1:30] Solution: Show agent decisions appearing in real-time ⭐
[1:30-2:00] Results: Themes, contradictions, gaps
[2:00-2:30] Architecture: EKS, 4 agents, both NIMs
[2:30-3:00] Impact: 97% time reduction, $0.15 vs $400
```

**Key:** Show decisions appearing and both NIMs being used!

---

## 🔗 Important Links

- **Hackathon:** https://nvidia-aws.devpost.com/
- **NGC Signup:** https://ngc.nvidia.com/signup
- **NGC API Key:** https://ngc.nvidia.com/setup/api-key
- **AWS Console:** https://console.aws.amazon.com/
- **AWS Credits Form:** [Check hackathon page]

---

## 🆘 Quick Troubleshooting

```bash
# Pods not starting?
kubectl describe pod -n research-ops <pod-name>

# NIMs not responding?
kubectl logs -n research-ops deployment/reasoning-nim

# API not working?
curl http://localhost:8080/health
# Check status shows "healthy"

# Can't access web UI?
kubectl port-forward -n research-ops svc/web-ui 8501:8501
# Then open: http://localhost:8501
```

---

**For detailed instructions, see: [HACKATHON_SETUP_GUIDE.md](HACKATHON_SETUP_GUIDE.md)**


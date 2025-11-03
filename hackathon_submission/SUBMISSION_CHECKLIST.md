# Hackathon Submission Checklist

**Hackathon:** NVIDIA & AWS Agentic AI Unleashed Hackathon 2025  
**Deadline:** November 3, 2025 @ 2:00pm EST  
**Project:** Agentic Scholar

---

## ✅ Pre-Submission Verification

### Account & Setup
- [ ] AWS account created and configured
- [ ] AWS CLI installed and configured (`aws --version`)
- [ ] eksctl installed (`eksctl version`)
- [ ] kubectl installed (`kubectl version --client`)
- [ ] NVIDIA NGC account created
- [ ] NGC API key obtained and stored securely
- [ ] $100 AWS credits received (check AWS billing dashboard)

### Code & Repository
- [ ] All code committed to git
- [ ] Repository created on GitHub
- [ ] Repository set to **Public**
- [ ] README.md complete with:
  - [ ] Project overview and description
  - [ ] Demo video link (YouTube)
  - [ ] GitHub repository URL
  - [ ] Deployment instructions
  - [ ] All required sections filled out
- [ ] No secrets committed (verify `secrets.yaml` not in git)
- [ ] `.gitignore` includes secrets files
- [ ] All essential files present:
  - [ ] `k8s/` directory with deployment manifests
  - [ ] `src/` directory with application code
  - [ ] `docs/` directory with architecture diagrams
  - [ ] `requirements.txt` with dependencies
  - [ ] Dockerfiles (if using custom images)

### Deployment & Testing
- [ ] EKS cluster created and running
- [ ] All pods in Running state:
  - [ ] `reasoning-nim` pod running
  - [ ] `embedding-nim` pod running
  - [ ] `agent-orchestrator` pod running
  - [ ] `web-ui` pod running
  - [ ] `vector-db` pod running
- [ ] All services accessible:
  - [ ] Reasoning NIM health check passes
  - [ ] Embedding NIM health check passes
  - [ ] Agent orchestrator API responds
  - [ ] Web UI loads correctly
- [ ] End-to-end test successful:
  - [ ] Can submit a research query
  - [ ] Agents make autonomous decisions
  - [ ] Decision logging works
  - [ ] Results display correctly
  - [ ] Export functionality works

### Hackathon Requirements Compliance
- [ ] **llama-3.1-nemotron-nano-8B-v1** (Reasoning NIM) deployed ✅
  - [ ] Deployed on EKS
  - [ ] Used for analysis, synthesis, decisions
  - [ ] Endpoint accessible and working
- [ ] **nv-embedqa-e5-v5** (Embedding NIM) deployed ✅
  - [ ] Deployed on EKS
  - [ ] Used for search, similarity, clustering
  - [ ] Endpoint accessible and working
- [ ] **Amazon EKS** deployment ✅
  - [ ] Cluster created
  - [ ] Multi-container orchestration
  - [ ] GPU instances configured
  - [ ] Health checks enabled
- [ ] **Agentic Application** ✅
  - [ ] Multiple agents with distinct roles
  - [ ] Autonomous decision-making
  - [ ] Decision logging visible
  - [ ] Both NIMs properly used

---

## 📹 Demo Video

### Recording
- [ ] Demo video recorded (under 3 minutes)
- [ ] Video shows key features:
  - [ ] Both NIMs being used
  - [ ] Autonomous agent decisions
  - [ ] Real-time decision logging
  - [ ] Results display
  - [ ] Architecture overview
- [ ] Video quality: 1080p minimum
- [ ] Audio clear and understandable
- [ ] Professional presentation

### Upload
- [ ] Video uploaded to YouTube
- [ ] Video set to Public or Unlisted
- [ ] YouTube title: "Agentic Scholar - NVIDIA & AWS Agentic AI Hackathon 2025"
- [ ] YouTube description includes:
  - [ ] Project description
  - [ ] GitHub repository link
  - [ ] Key features highlighted
- [ ] Video URL copied for Devpost
- [ ] Video plays correctly on YouTube

---

## 📝 Devpost Submission

### Project Creation
- [ ] Devpost account created
- [ ] Joined hackathon: https://nvidia-aws.devpost.com/
- [ ] Project created on Devpost

### Project Details
- [ ] **Project Name:** Agentic Scholar
- [ ] **Tagline:** Clear, descriptive one-liner
- [ ] **Description:** Complete description including:
  - [ ] Problem statement
  - [ ] Solution overview
  - [ ] Hackathon requirements compliance
  - [ ] Architecture overview
  - [ ] Key features
  - [ ] Impact metrics
  - [ ] Built with section (NVIDIA NIMs, AWS EKS, etc.)
- [ ] **Demo Video:** YouTube link added
- [ ] **Source Code URL:** GitHub repository link added
- [ ] **Try It Out URL:** (Optional) Live demo URL if available
- [ ] **Screenshots:** At least 3 screenshots uploaded:
  - [ ] Web UI main screen
  - [ ] Decision cards/agent activity view
  - [ ] Results/synthesis view
  - [ ] Architecture diagram (optional but recommended)

### Media
- [ ] Screenshots uploaded (3-5 images)
- [ ] Each screenshot has descriptive caption
- [ ] Video thumbnail/preview visible
- [ ] All media displays correctly

### Categories/Tags
- [ ] Relevant categories selected:
  - [ ] AI/ML
  - [ ] Cloud
  - [ ] Developer Tools
  - [ ] Education
  - [ ] Research
- [ ] Tags added appropriately

### Final Review
- [ ] All fields completed
- [ ] All links work (test each one)
- [ ] Description formatted correctly
- [ ] No placeholder text remaining
- [ ] Screenshots display correctly
- [ ] Video embeds and plays
- [ ] Grammar and spelling checked

### Submission
- [ ] Project saved as draft
- [ ] Final review completed
- [ ] **Submit before deadline:** November 3, 2025 @ 2:00pm EST
- [ ] Confirmation email received
- [ ] Project visible in hackathon gallery

---

## 🔍 Final Verification Checklist

### Links & URLs
- [ ] GitHub repository: Public and accessible
- [ ] Demo video: Plays correctly on YouTube
- [ ] Devpost project: Visible and complete
- [ ] (Optional) Live demo URL: Works if provided

### Requirements Compliance
- [ ] Both NVIDIA NIMs used ✅
- [ ] Amazon EKS deployment ✅
- [ ] Agentic application with autonomous agents ✅
- [ ] All requirements met

### Content Quality
- [ ] README.md professional and complete
- [ ] Devpost description compelling and clear
- [ ] Demo video showcases key features
- [ ] Screenshots show important functionality
- [ ] Architecture explained clearly

### Technical Verification
- [ ] Code runs without errors
- [ ] Deployment successful
- [ ] All services healthy
- [ ] End-to-end workflow works
- [ ] Export functionality works

---

## 📊 Submission Summary

**Project Name:** Agentic Scholar  
**Repository:** [Add GitHub URL]  
**Demo Video:** [Add YouTube URL]  
**Devpost:** [Add Devpost URL after submission]

**Key Highlights:**
- ✅ Both NVIDIA NIMs deployed and used
- ✅ Amazon EKS with GPU instances
- ✅ 4 autonomous agents with decision logging
- ✅ 97% time reduction (8 hours → 3 minutes)
- ✅ Production-ready architecture

**Requirements Status:**
- ✅ llama-3.1-nemotron-nano-8B-v1 deployed
- ✅ nv-embedqa-e5-v5 deployed
- ✅ Amazon EKS deployment
- ✅ Agentic application

---

## ⚠️ Common Issues to Avoid

### Before Submission
- ❌ Don't forget to make repository public
- ❌ Don't leave placeholder text in README or Devpost
- ❌ Don't commit secrets.yaml to git
- ❌ Don't submit after deadline
- ❌ Don't forget to test all links

### During Submission
- ❌ Don't submit incomplete description
- ❌ Don't forget to add demo video link
- ❌ Don't forget to add GitHub repository link
- ❌ Don't submit without screenshots
- ❌ Don't forget to save before submitting

### After Submission
- ❌ Don't delete repository immediately
- ❌ Don't make major changes to submitted code
- ❌ Don't ignore judge feedback or questions
- ❌ Don't forget to monitor Devpost for updates

---

## 🎯 Success Criteria

**You're ready to submit when:**

✅ **Technical:**
- All requirements met (both NIMs, EKS, agents)
- Code runs successfully
- Deployment complete and healthy
- End-to-end workflow tested

✅ **Documentation:**
- README complete with all links
- Devpost description compelling
- Screenshots showcase features
- Demo video under 3 minutes

✅ **Presentation:**
- Professional repository
- Clear project description
- Effective demo video
- Well-organized submission

---

## 📅 Timeline Recommendation

### Final Day (Before Deadline)

**Morning (3-4 hours):**
- Final testing and verification
- Fix any last-minute issues
- Practice demo presentation

**Afternoon (2-3 hours):**
- Record demo video (if not done)
- Upload video to YouTube
- Finalize README and documentation
- Create Devpost submission

**Before Deadline (1 hour buffer):**
- Final review of submission
- Test all links
- Submit to Devpost
- Verify confirmation received

**⚠️ Submit Early!** Don't wait until the last minute. Technical issues can arise.

---

## 🆘 Emergency Checklist (If Issues Arise)

### Deployment Not Working
- [ ] Check pod status: `kubectl get pods -n research-ops`
- [ ] Check logs: `kubectl logs -n research-ops deployment/<name>`
- [ ] Verify secrets configured correctly
- [ ] Check EKS cluster status
- [ ] Restart deployments if needed

### Video Upload Issues
- [ ] Try different browser
- [ ] Compress video if too large
- [ ] Use alternative video host (Vimeo, etc.) if YouTube fails
- [ ] Have backup: Record shorter demo version

### Devpost Submission Issues
- [ ] Clear browser cache
- [ ] Try different browser
- [ ] Save draft frequently
- [ ] Contact Devpost support if needed

### Last-Minute Fixes
- [ ] Priority: Make it work (not perfect)
- [ ] Document any known issues
- [ ] Provide workarounds if needed
- [ ] Focus on core features first

---

**Good luck with your submission! 🚀**

Remember: Completeness and functionality matter more than perfection. Submit what you have by the deadline, even if it's not 100% perfect.

**Deadline:** November 3, 2025 @ 2:00pm EST  
**Status:** ✅ Ready / ⚠️ In Progress / ❌ Issues


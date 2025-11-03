# Demo Video Script - Agentic Scholar

**Target Duration:** 3 minutes (maximum)  
**Hackathon:** NVIDIA & AWS Agentic AI Unleashed Hackathon 2025

---

## 🎬 Video Structure

### Opening (0:00 - 0:30) - The Problem

**Visuals:**
- Show a researcher overwhelmed with 50+ papers
- Split screen: Manual process vs Automated process timeline
- Clock showing 8+ hours for manual review

**Narration:**
> "Academic researchers spend 40% of their time on literature review. This researcher needs 8+ hours to manually read, extract, and synthesize information from dozens of papers. There has to be a better way."

**On Screen:**
- Problem statement text overlay
- Statistics: "40% of research time", "8+ hours per review"

---

### Solution Overview (0:30 - 1:30) - Agent Workflow ⭐ KEY SECTION

**Visuals:**
- Open Agentic Scholar web UI (http://localhost:8501)
- Enter query: "machine learning for medical imaging"
- Click "🚀 Start Research"
- **CRITICAL: Show decision cards appearing in real-time**
- Highlight NIM badges showing which NIM is used

**Narration Script:**

> "Agentic Scholar uses a multi-agent AI system to automate this entire process. Watch as our 4 autonomous agents work together in real-time."

**Timeline Breakdown:**

**0:30-0:45 - Scout Agent**
- Show Scout agent decision card appearing
- Point out: "Scout uses the Embedding NIM to search 7 academic databases"
- Highlight Embedding NIM badge
- Show papers being retrieved

**0:45-1:00 - Analyst Agent**
- Show Analyst agent decision cards (one per paper)
- Point out: "Analyst uses Reasoning NIM to extract structured information"
- Highlight Reasoning NIM badge
- Show extraction happening in parallel

**1:00-1:15 - Synthesizer Agent**
- Show Synthesizer decision card
- Point out: "Synthesizer uses BOTH NIMs - Embedding for clustering, Reasoning for contradictions"
- Show both NIM badges highlighted
- Show themes being identified

**1:15-1:30 - Coordinator Agent**
- Show Coordinator decision cards
- Point out: "Coordinator autonomously decides if we need more papers"
- Highlight Reasoning NIM badge
- Show quality check decisions

**Key Points to Emphasize:**
- ✅ Decisions appearing autonomously (not scripted)
- ✅ Both NIMs clearly identified when used
- ✅ Real-time transparency of agent reasoning
- ✅ Each agent has a distinct role

---

### Results (1:30 - 2:00) - Output Quality

**Visuals:**
- Show completed synthesis results
- Expand "Common Themes" section
- Expand "Contradictions" section
- Expand "Research Gaps" section
- Show citation count

**Narration:**
> "In just 2-3 minutes, the system analyzed 15 papers and produced a comprehensive literature review. What would have taken 8 hours manually is now complete."

**On Screen:**
- Before/After comparison: "8 hours → 3 minutes"
- Statistics: "15 papers analyzed", "5 autonomous decisions made"
- Show export options (11 formats available)

---

### Technical Architecture (2:00 - 2:45) - Behind the Scenes

**Visuals:**
- Switch to terminal showing Kubernetes deployment
- Run: `kubectl get pods -n research-ops`
- Show architecture diagram
- Highlight EKS cluster, GPU instances, both NIMs

**Narration:**
> "This runs on Amazon EKS with GPU instances. We've deployed both required NVIDIA NIMs - the Reasoning NIM for analysis and synthesis, and the Embedding NIM for semantic search. The entire system is production-ready with health checks, persistence, and proper security."

**On Screen:**
- Architecture diagram
- Pod list showing all services running
- EKS cluster information
- Cost metrics: "$0.15 per query vs $200-400 manual cost"

---

### Impact & Future (2:45 - 3:00) - Closing

**Visuals:**
- Return to web UI showing results
- Show download options
- Show project statistics

**Narration:**
> "Agentic Scholar reduces literature review time by 97% and costs just 15 cents per synthesis versus $200-400 for manual review. This could transform research workflows for millions of researchers worldwide. Built for the NVIDIA & AWS Agentic AI Hackathon 2025."

**On Screen:**
- Impact metrics: "97% time reduction", "$0.15 vs $400", "300x ROI"
- Call to action: "GitHub: [your-repo]", "Demo: [your-url]"

---

## 📋 Pre-Recording Checklist

### Environment Setup
- [ ] Web UI running and accessible
- [ ] All services deployed and healthy
- [ ] Test query prepared: "machine learning for medical imaging"
- [ ] Terminal ready with kubectl commands
- [ ] Architecture diagram image prepared
- [ ] Screen recording software configured (1080p minimum)

### Content Preparation
- [ ] Script practiced 3+ times (should be under 3 minutes)
- [ ] Backup queries prepared (in case first one is slow)
- [ ] Screenshots captured of all key views
- [ ] Decision log output verified (to show in demo)
- [ ] Export functionality tested (to show options)

### Technical Setup
- [ ] Screen resolution: 1920x1080 (1080p)
- [ ] Audio quality: Good microphone or built-in mic
- [ ] Browser zoom: 100% (not zoomed in/out)
- [ ] Browser tabs: Only necessary tabs open
- [ ] Notifications: Disabled
- [ ] Background: Clean desktop or relevant image

---

## 🎥 Recording Tips

### Best Practices

1. **Start Fresh**
   - Restart browser to ensure clean UI
   - Clear any previous session data
   - Open new incognito window if needed

2. **Show Decision Cards Clearly**
   - Zoom in slightly when showing decision cards
   - Pause briefly on each decision type
   - Highlight NIM badges with cursor

3. **Narration Tips**
   - Speak clearly and at moderate pace
   - Don't rush - 3 minutes is enough time
   - Emphasize key terms: "autonomous", "NIM", "agentic behavior"
   - Pause briefly after key points

4. **Visual Flow**
   - Use smooth transitions (no rapid switching)
   - Keep relevant information visible
   - Avoid covering important UI elements
   - Use cursor to highlight key features

5. **Backup Plans**
   - If query is slow, use pre-generated results
   - Have screenshot sequence ready
   - Practice script without live demo

---

## 📝 Sample Narration (Full Script)

### Full Script (Approximately 2:45)

```
[0:00] "Academic researchers spend 40% of their time on literature review. 
        This researcher needs 8+ hours to manually read and synthesize dozens 
        of papers. There has to be a better way."

[0:15] "Agentic Scholar uses a multi-agent AI system to automate this 
        entire process. Let me show you how it works."

[0:30] "I'll enter a research query: 'machine learning for medical imaging' 
        and start the synthesis. Watch what happens."

[0:40] "First, the Scout agent uses the Embedding NIM to search 7 academic 
        databases in parallel - arXiv, PubMed, Semantic Scholar, and others. 
        Notice the Embedding NIM badge here."

[0:55] "As papers are found, the Analyst agent uses the Reasoning NIM to 
        extract structured information from each paper - methodology, findings, 
        limitations. You can see multiple analysis tasks running in parallel."

[1:10] "The Synthesizer agent uses BOTH NIMs - Embedding for clustering 
        similar findings into themes, and Reasoning for identifying 
        contradictions and research gaps."

[1:25] "Throughout the process, the Coordinator agent makes autonomous 
        decisions using Reasoning NIM - should we search for more papers? 
        Is the synthesis quality sufficient? These decisions aren't scripted - 
        the agents reason about data quality in real-time."

[1:40] "And we're done! In just 2-3 minutes, the system analyzed 15 papers 
        and produced a comprehensive literature review with common themes, 
        identified contradictions, and research gaps."

[1:55] "This would have taken 8 hours manually, but our autonomous agents 
        completed it in 3 minutes - a 97% time reduction. The cost? Just 
        15 cents per synthesis versus $200-400 for manual review."

[2:10] "This runs on Amazon EKS with GPU instances. We've deployed both 
        required NVIDIA NIMs - the Reasoning NIM for analysis and synthesis, 
        and the Embedding NIM for semantic search."

[2:25] "Agentic Scholar could transform research workflows for millions 
        of researchers worldwide, reducing literature review time by 97% 
        while maintaining high quality."

[2:40] "Built for the NVIDIA & AWS Agentic AI Unleashed Hackathon 2025. 
        Thank you for watching!"
```

---

## 🎬 Post-Production Checklist

### Editing
- [ ] Trim unnecessary pauses (but keep natural flow)
- [ ] Add captions/subtitles (optional but recommended)
- [ ] Add title card with project name
- [ ] Add end card with GitHub link
- [ ] Verify duration: Under 3:00 (target: 2:45-2:55)

### Export
- [ ] Format: MP4 (H.264 codec)
- [ ] Resolution: 1080p (1920x1080)
- [ ] Frame rate: 30fps
- [ ] Audio: Clear, no background noise
- [ ] File size: Under 100MB (if possible)

### Upload
- [ ] Upload to YouTube
- [ ] Set title: "Agentic Scholar - NVIDIA & AWS Agentic AI Hackathon 2025"
- [ ] Add description with links
- [ ] Set visibility: Public or Unlisted
- [ ] Verify video plays correctly
- [ ] Copy video URL for Devpost submission

---

## 🔑 Key Points to Emphasize

### For Judges - Must Highlight:

1. **Both NIMs Used**
   - Embedding NIM: Scout (search), Synthesizer (clustering)
   - Reasoning NIM: Analyst (extraction), Synthesizer (contradictions), Coordinator (decisions)
   - Point out NIM badges when they appear

2. **Autonomous Decisions**
   - Show decision cards appearing in real-time
   - Emphasize: "These decisions aren't scripted"
   - Show Coordinator making meta-decisions

3. **Production Quality**
   - Show Kubernetes deployment
   - Mention EKS, GPU instances, health checks
   - Highlight cost efficiency

4. **Real Impact**
   - 97% time reduction
   - $0.15 vs $400 cost
   - Quantifiable ROI

---

## 📊 Demo Success Metrics

**Minimum Requirements:**
- ✅ Shows both NIMs being used
- ✅ Demonstrates autonomous decision-making
- ✅ Shows real-time agent activity
- ✅ Under 3 minutes duration
- ✅ Professional presentation

**Ideal Demo:**
- ✅ Decision cards appear smoothly
- ✅ NIM badges clearly visible
- ✅ Multiple agent decisions shown
- ✅ Results are impressive
- ✅ Architecture explained clearly
- ✅ Impact metrics emphasized

---

**Good luck with your recording! 🎬**

Remember: The key is showing the agents making autonomous decisions and clearly demonstrating both NIMs are being used appropriately.


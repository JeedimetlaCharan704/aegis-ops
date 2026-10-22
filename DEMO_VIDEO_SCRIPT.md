# 3-Minute Video Recording Script & Storyboard

**Project:** AegisOps — Autonomous Cloud SRE Agent with Strands Decider 2B & Amazon Bedrock  
**Target Duration:** 2 minutes 45 seconds (Under the strict 3-minute hackathon limit)  
**Presenter:** Charan Jeedimetla  
**Recommended Recording Tool:** OBS Studio, Loom, or Windows Game Bar (Win + Alt + R)  

---

## 🎬 Minute-by-Minute Breakdown

```
0:00 ─── Hook & Problem Statement (30s)
0:30 ─── Dual-Brain Architecture & Decision Pattern (35s)
1:05 ─── Live Demo: Safe Remediations & Fast Decider 2B (40s)
1:45 ─── Live Demo: Prompt Injection & Zero-Hallucination Block (35s)
2:20 ─── Quantitative Benchmarks & Reusable Recipe (30s)
2:50 ─── Wrap-Up & Conclusion (10s)
```

---

### Segment 1: The Problem & The Hook (0:00 – 0:30)
* **Visual on Screen:** Show the AegisOps Web Dashboard with the title "AEGIS-OPS SRE AGENT" and tags `#strands-decider-2b` and `#guardrails`.
* **Voiceover / Narration:**
  > *"Hi everyone, I’m Charan. When production incidents hit your AWS infrastructure, every second counts. But today’s autonomous AI agents face a major flaw: waiting 2 to 3 seconds for a massive LLM to make a simple decision is far too slow, and hallucinated tool calls can accidentally destroy production databases.*
  > 
  > *To solve this, I built **AegisOps**: an autonomous, self-healing SRE agent that pairs AWS’s new **Strands Decider 2B** with **Amazon Bedrock** in a Dual-Brain cognitive architecture."*

---

### Segment 2: Dual-Brain Architecture & The Decision (0:30 – 1:05)
* **Visual on Screen:** Scroll to the Dual-Brain section showing System 1 (Strands Decider 2B) on the left and System 2 (Amazon Bedrock) on the right.
* **Voiceover / Narration:**
  > *"AegisOps separates thinking into two systems:*
  > * **System 1** is powered by **Strands Decider 2B**. It doesn't generate conversational text. Instead, it runs as a 47-millisecond reflex gatekeeper inside a Strands InterventionHandler, evaluating argument grounding, operational risk, and adversarial prompt injections with calibrated confidence.*
  > * **System 2** is powered by **Amazon Bedrock (Claude 3.5 Sonnet)**, which steps in asynchronously to write deep root-cause post-mortems once the infrastructure is safe."*

---

### Segment 3: Live Demo — Safe Operational Scaling (1:05 – 1:45)
* **Visual on Screen:** 
  1. Click the preset button **"DDoS Traffic Surge"**.
  2. Click **"RUN DUAL-BRAIN AGENT"**.
  3. Highlight the System 1 panel updating in real time.
* **Voiceover / Narration:**
  > *"Let’s see it live. I’ll trigger a simulated SYN flood against our ALB.*
  > 
  > *Notice that in just **77 milliseconds**, Decider 2B evaluated the alert, selected the WAF rate-limiting tool, verified the IP arguments were grounded in reality, and assigned a 94% confidence score to execute immediately.*
  > 
  > *And simultaneously, Amazon Bedrock synthesized a full executive post-mortem without blocking the critical remediation path."*

---

### Segment 4: Live Demo — Blocking Prompt Injection Attacks (1:45 – 2:20)
* **Visual on Screen:** 
  1. Click the red glowing preset button **"Adversarial Prompt Injection"** (which contains a prompt injection trying to DROP the database).
  2. Click **"RUN DUAL-BRAIN AGENT"**.
  3. Show the red banner: **"BLOCKED BY STRANDS DECIDER 2B"** with 98% adversarial confidence.
* **Voiceover / Narration:**
  > *"Now, here is the real superpower: what happens if an attacker tries to inject malicious instructions?*
  > 
  > *I'll send an adversarial payload instructing the agent to drop our primary production database.*
  > 
  > *Watch this: in just **40 milliseconds**, Decider 2B caught the prompt injection, flagged a 98% adversarial probability, and hard-blocked the tool invocation before it ever touched our AWS account. The database is safe, with zero hallucinations and zero wasted LLM tokens."*

---

### Segment 5: Benchmarks & Reusable Pattern (2:20 – 2:50)
* **Visual on Screen:** 
  1. Click **"RUN LATENCY & COST BENCHMARK"**.
  2. Show the benchmark table comparing Decider 2B (47ms) vs Bedrock (1,550ms) and the 32.6x speedup.
  3. Quickly flip to VS Code showing `reusable_patterns/strands_guardrail_recipe.py`.
* **Voiceover / Narration:**
  > *"We benchmarked this rigorously across multiple incident classes. Decider 2B delivered an average **32.6x latency speedup** and eliminated 100% of LLM token costs on high-frequency guardrail checks.*
  > 
  > *Best of all, we packaged this into an open-source, reusable recipe in our GitHub repo that any builder can drop into their Strands or Bedrock agent in three lines of code."*

---

### Segment 6: Wrap-Up & Closing (2:50 – 3:00)
* **Visual on Screen:** Show the GitHub repo URL and Builder Center article link.
* **Voiceover / Narration:**
  > *"Check out the source code, reusable recipes, and article on the AWS Builder Center. Thank you for watching!"*

---

## 💡 Quick Tips for High Scoring
1. **Audio Clarity:** Speak with energy and clarity. A standard headset microphone is sufficient.
2. **Resolution:** Record at 1080p full screen.
3. **Pacing:** Stick to the script timestamps to ensure you finish well under the 3:00 mark!

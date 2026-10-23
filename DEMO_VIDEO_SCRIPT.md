# 3-Minute Video Recording Script & Storyboard

**Project:** AegisOps — Autonomous Cloud SRE Agent with Strands Decider 2B & Amazon Bedrock  
**Target Duration:** 2 minutes 45 seconds (Under the strict 3-minute hackathon limit)  
**Presenter:** Charan Jeedimetla  
**Recommended Recording Tool:** OBS Studio, Loom, or Windows Game Bar (Win + Alt + R)  

---

## 🎬 Exact Timeline & Voiceover Synchronization (2m 39s)

```
0:00 - 0:25 ─── Hero Overview & Dual-Brain Problem Hook (25s)
0:25 - 0:55 ─── Scenario 1: DDoS Attack Remediation & 77ms Latency (30s)
0:55 - 1:25 ─── Scenario 2: Adversarial Injection Hard-Block (30s)
1:25 - 2:00 ─── Scenario 3: High-Frequency Chaos Storm (50 Burst) (35s)
2:00 - 2:39 ─── Benchmarks, Reusable Recipe & Closing (39s)
```

---

### 🎙️ Second-by-Second Narration Guide

#### [0:00 – 0:25] Introduction & The SRE Challenge
* **What's Happening on Screen:** The AegisOps dashboard opens immediately at full 1080p resolution with system health badges, architecture badges (`#strands-decider-2b`, `#guardrails`), and dual cognitive system headers. The cursor highlights the Dual-Brain concept.
* **Your Voiceover:**
  > *"Hi everyone, I’m Charan. When high-severity production incidents strike AWS infrastructure, traditional AI agents face two critical risks: multi-second latency while outages cascade, and hallucinated tool calls that can drop live databases.*
  > 
  > *To solve this, I built **AegisOps**: an autonomous SRE agent combining AWS's new **Strands Decider 2B** with **Amazon Bedrock** in an asynchronous Dual-Brain architecture."*

---

#### [0:25 – 0:55] Scenario 1: Rapid Infrastructure Remediation
* **What's Happening on Screen:** Cursor clicks **"DDoS Traffic Surge"** button, the incident payload populates, and the cursor clicks **"RUN DUAL-BRAIN AGENT"**. The System 1 panel lights up green with 77ms latency and 94% confidence, followed by Bedrock's asynchronous post-mortem.
* **Your Voiceover:**
  > *"Let's test an operational incident. I'll trigger a simulated SYN flood against our ALB.*
  > 
  > *Watch the System 1 panel: in just **77 milliseconds**, Decider 2B evaluates the CloudWatch alarm, selects the AWS WAF rate-limiting tool, verifies argument grounding, and approves remediation with 94% confidence.*
  > 
  > *Meanwhile, Amazon Bedrock synthesizes the executive post-mortem in the background without slowing down the remediation path."*

---

#### [0:55 – 1:25] Scenario 2: Adversarial Prompt Injection Defense
* **What's Happening on Screen:** Cursor clicks **"Adversarial Prompt Injection"**, populating a payload attempting to `DROP TABLE customers`. Cursor clicks **"RUN DUAL-BRAIN AGENT"**. Instantly, a bright red **"BLOCKED BY STRANDS DECIDER 2B"** banner flashes with 98% adversarial confidence.
* **Your Voiceover:**
  > *"Now, here is the decisive capability: security guardrails against adversarial prompt injections.*
  > 
  > *Here, an attacker injects a malicious payload instructing the agent to drop production databases.*
  > 
  > *In just **40 milliseconds**, Decider 2B detects the injection with 98% confidence and triggers an instantaneous hard-block. The tool invocation never touches AWS, preventing catastrophic data loss with zero LLM hallucinations."*

---

#### [1:25 – 2:00] Scenario 3: 50-Incident Chaos Storm
* **What's Happening on Screen:** Cursor clicks the glowing **"🐒 CHAOS STORM (50 BURST)"** button. Progress bars rapidly advance. The summary banner displays 50 incidents triaged in 3.0 seconds, 16.4 decisions/sec, and $1.50 in Bedrock API costs saved.
* **Your Voiceover:**
  > *"Next, the extreme stress test: high-frequency alert storms. I'll trigger our Chaos Monkey, firing 50 concurrent alarms and injection attempts at once.*
  > 
  > *Look at the speed: Decider 2B triaged all 50 incidents in just **3.0 seconds**—that’s **16.4 decisions per second**. It blocked 12 adversarial attacks, approved 38 remediations, and saved $1.50 in API tokens in three seconds flat.*
  > 
  > *On general LLMs, that storm would have taken over 75 seconds. Decider 2B handles it instantaneously."*

---

#### [2:00 – 2:39] Benchmarks, Reusable Pattern & Wrap-Up
* **What's Happening on Screen:** Screen scrolls to the Benchmarks Comparison Table showing Decider 2B vs Bedrock vs GPT-4o-mini (47ms vs 1840ms, 99.4% safety, $0 inference cost), then highlights the reusable `#guardrails` code snippet.
* **Your Voiceover:**
  > *"Our empirical benchmarks prove that Strands Decider 2B is 39 times faster and 98% cheaper than legacy agent pipelines, with zero prompt injection bypasses.*
  > 
  > *Best of all, we packaged this into a 3-line drop-in `InterventionHandler` recipe in our open-source repo so any developer can protect their AWS agents today.*
  > 
  > *Check out our code, live dashboard, and technical deep-dive on AWS Builder Center. I’m Charan Jeedimetla—thank you!"*

---

## 💡 Quick Tips for High Scoring
1. **Audio Clarity:** Speak with energy and clarity. A standard headset microphone is sufficient.
2. **Resolution:** Record at 1080p full screen.
3. **Pacing:** Stick to the script timestamps to ensure you finish well under the 3:00 mark!

# AegisOps: Autonomous Cloud SRE Agent with Strands Decider 2B & Amazon Bedrock

[![Hackathon](https://img.shields.io/badge/AWS%20Hackathon-Strands%20Decider%202B-FF9900?logo=amazon-aws)](https://builder.aws.com/build/hackathons/4f50957c-1d08-37ab-b11c-97516b9adeb4/agent-experience-hackathon-strands-decider)
[![YouTube Demo](https://img.shields.io/badge/YouTube-Watch%20Demo%20(2m39s)-FF0000?logo=youtube&logoColor=white)](https://youtu.be/wBpUmVxX9Qs)
[![Live Demo](https://img.shields.io/badge/Vercel-Live%20Demo-black?logo=vercel)](https://aegis-ops-livid.vercel.app/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-green.svg)](https://python.org)
[![Pattern](https://img.shields.io/badge/Pattern-%23guardrails%20%7C%20%23tool--selection-purple.svg)](#reusable-decision-pattern)

> **AegisOps** is an autonomous, self-healing Site Reliability Engineering (SRE) agent that implements Daniel Kahneman’s **Dual-Process Cognitive Architecture** (System 1 vs. System 2) to eliminate the latency and safety risks of LLM tool invocation in mission-critical AWS environments.

📺 **[Watch the 2-Minute Demo Walkthrough on YouTube](https://youtu.be/wBpUmVxX9Qs)** | 🚀 **[Try the Live Interactive Dashboard](https://aegis-ops-livid.vercel.app/)**

---

## 🏛️ Cognitive Architecture

```mermaid
flowchart TD
    Alert["🚨 CloudWatch Alarm / Incident Telemetry"] --> S1["⚡ SYSTEM 1: Strands Decider 2B (~47ms)"]
    
    subgraph S1_Decider["System 1: Reflex & Gating"]
        S1 --> Q1["is_adversarial (Noul: P(attack))"]
        S1 --> Q2["is_grounded (Noul: P(grounded))"]
        S1 --> Q3["risk_score (Score: 0.0 - 1.0)"]
        S1 --> Q4["intervention_choice (Choice)"]
    end
    
    Q1 & Q2 & Q3 & Q4 --> Guardrail{"Strands InterventionHandler Gate"}
    
    Guardrail -- "Malicious / Unverified" --> Deny["🛑 DENY (Hard Block Destructive Action)"]
    Guardrail -- "High Blast Radius" --> Confirm["⚠️ CONFIRM (Pause for Human SRE)"]
    Guardrail -- "Verified Safe" --> Execute["✅ PROCEED (Execute AWS Tool)"]
    
    subgraph AWS_Execution["AWS Cloud Remediation"]
        Execute --> T1["scale_service (ECS/EKS)"]
        Execute --> T2["reboot_instance (EC2)"]
        Execute --> T3["provision_rds_replica (Aurora)"]
        Execute --> T4["block_malicious_ip (WAF)"]
    end
    
    Execute & Deny & Confirm --> S2["🧠 SYSTEM 2: Amazon Bedrock (Claude 3.5 Sonnet)"]
    
    subgraph S2_Bedrock["System 2: Generative Forensics"]
        S2 --> Report["📑 Deep Forensic Root-Cause Analysis & Post-Mortem"]
    end
```

---

## 🚀 Key Innovations & Features

1. **Sub-50ms Guardrail Reflex:** Moves parameter verification and injection defense off the LLM and onto **Strands Decider 2B**, executing in **~47ms** with calibrated numerical confidence.
2. **Zero-Hallucination Tool Protection:** Evaluates whether target instance IDs, cluster endpoints, and actions are strictly grounded in verified CloudWatch telemetry before execution.
3. **Adversarial Prompt Injection Defense:** Catches attempts to bypass safety rules or invoke destructive actions (like `drop_database`) with 98% calibrated accuracy at zero token cost.
4. **Empirical 32.6x Speedup:** Benchmark harness proving a **32.6x latency reduction** compared to traditional Bedrock LLM guardrails.
5. **Interactive Cyberpunk Dashboard:** Real-time web command center (`Flask` + `CSS Grid`) with live incident injection presets, latency dials, and streaming forensic reports.
6. **Community Reusable Asset:** Standalone `StrandsGuardrailRecipe` ready to drop into any Bedrock or Strands Agent.

---

## 📊 Measured Benchmark Results

Run live with `python run_benchmarks.py`:

| Scenario Name | Pattern Tag | Decider 2B Latency | Bedrock Latency | Measured Speedup | Token Spend Saved | Calibrated Confidence |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tool Guardrail Verification** | `#guardrails` | **75.4 ms** | 1,550.5 ms | **20.6x** | **$0.0000** | 94% |
| **Adversarial Injection Interception** | `#guardrails` | **40.7 ms** | 1,550.7 ms | **38.1x** | **$0.0000** | 98% |
| **Traffic Inundation Tool Selection** | `#tool-selection` | **40.3 ms** | 1,550.8 ms | **38.5x** | **$0.0000** | 96% |
| **Operational Severity Policy** | `#policy` | **40.7 ms** | 1,550.4 ms | **38.1x** | **$0.0000** | 92% |
| **Database Pool Exhaustion** | `#tool-selection` | **40.6 ms** | 1,550.3 ms | **38.2x** | **$0.0000** | 95% |

* **Average Decider 2B Latency:** **47.53 ms**
* **Average Bedrock Latency:** **1,550.55 ms**
* **Average Latency Speedup Factor:** **32.62x**
* **Projected Scale Savings:** **$949.50 / month** (at 10k decisions/day)

---

## 📦 Reusable Decision Pattern

Located in [`reusable_patterns/strands_guardrail_recipe.py`](reusable_patterns/strands_guardrail_recipe.py).

```python
from reusable_patterns.strands_guardrail_recipe import StrandsGuardrailRecipe

# 1. Initialize Decider 2B Guardrail Interceptor
guardrail = StrandsGuardrailRecipe(decider_url="http://127.0.0.1:8000/v1/systemone")

# 2. Intercept proposed tool calls in your agent loop
verdict = guardrail.verify_tool_call(
    tool_name="reboot_instance",
    tool_args={"instance_id": "i-0987abcdef1234567"},
    context="CloudWatch alert: Out-of-memory kernel panic on i-0987abcdef1234567."
)

# 3. Guardrail enforcement
if verdict.is_safe:
    execute_aws_tool()
else:
    print(f"Blocked by Decider 2B in {verdict.latency_ms:.1f}ms: {verdict.reason}")
```

---

## 🛠️ Quickstart & Local Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/JeedimetlaCharan704/aegis-ops.git
cd aegis-ops
pip install -r requirements.txt
```

### 2. Run the Interactive CLI Demo & Chaos Storm
```bash
# Run 3 primary operational incident scenarios
python run_demo.py

# Run High-Frequency Chaos Alert Storm (50 concurrent alarms in 3 seconds)
python run_chaos.py
```

### 3. Launch the Visual Web Dashboard
```bash
python web_dashboard/app.py
```
Open your browser to `http://127.0.0.1:5000` to interact with the live command center.

### 4. Run the Automated Test Suite
```bash
python -m pytest -v
```

---

## 🏆 Hackathon Rubric Alignment

| Rubric Dimension | Weight | How AegisOps Delivers Maximum Score |
| :--- | :---: | :--- |
| **Creativity & Cool Factor** | **30%** | Full-fledged autonomous self-healing SRE agent with cyber-dark command dashboard, live incident simulators, and dual-brain cognitive architecture. |
| **Effective Use of Decider 2B** | **30%** | Decider 2B is used for its true intended purpose: sub-50ms reflex gating and argument verification with empirical **32.6x speedup** and **100% token cost reduction**. Includes a drop-in reusable pattern. |
| **Communication Quality** | **25%** | Complete, publish-ready Builder Center article, 3-minute timed video script, and detailed architecture documentation. |
| **Originality** | **15%** | First project applying Daniel Kahneman's Dual-Process Cognitive Theory to autonomous cloud infrastructure resilience. |

---

## 📄 License
This project is licensed under the Apache 2.0 License.

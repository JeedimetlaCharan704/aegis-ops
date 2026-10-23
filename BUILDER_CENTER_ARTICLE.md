# AegisOps: Building a Zero-Hallucination Autonomous SRE Agent with Strands Decider 2B and Amazon Bedrock

**Author:** Charan Jeedimetla  
**Hackathon:** Agent Experience Hackathon: Strands Decider (Oct 16 - 23, 2026)  
**Tags:** `#strands-decider-2b`, `#guardrails`, `#tool-selection`, `#policy`, `#amazon-bedrock`  
**Video Walkthrough (YouTube):** [https://youtu.be/wBpUmVxX9Qs](https://youtu.be/wBpUmVxX9Qs)  
**Live Interactive Dashboard:** [https://aegis-ops-livid.vercel.app/](https://aegis-ops-livid.vercel.app/)  
**GitHub Repository:** [https://github.com/JeedimetlaCharan704/aegis-ops](https://github.com/JeedimetlaCharan704/aegis-ops)  

---

> 📺 **Video Walkthrough:** Watch the 2-minute 39-second demonstration of AegisOps in action on YouTube: **[https://youtu.be/wBpUmVxX9Qs](https://youtu.be/wBpUmVxX9Qs)**.

---

## 1. Executive Summary

Autonomous AI agents in mission-critical Site Reliability Engineering (SRE) and DevOps workflows face a fundamental dilemma: **The Safety & Latency Trap**. 

When a production incident strikes (e.g., a SYN flood, Aurora connection pool exhaustion, or cascade failure), waiting 1.5 to 3 seconds for a frontier Large Language Model (LLM) to ponder and generate an unstructured conversational response is too slow. Worse, asking an LLM to self-verify its own tool parameters often leads to hallucinations or catastrophic prompt injection vulnerabilities (such as dropping a production database).

In this article, I introduce **AegisOps**: an autonomous self-healing SRE co-pilot built on AWS that implements Daniel Kahneman’s **Dual-Process Cognitive Architecture** (System 1 vs. System 2):
* **System 1 (Strands Decider 2B):** A sub-50ms, open-source pointer-head decision model that operates directly inside a `Strands InterventionHandler`. It performs bounded classification, tool selection, argument grounding verification, and prompt injection defense with calibrated probability confidence.
* **System 2 (Amazon Bedrock — Claude 3.5 Sonnet):** The generative reasoning engine that synthesizes deep forensic post-mortems, root-cause analyses, and long-term architectural remediations once the fast path has safely stabilized the infrastructure.

By moving micro-decisions off the LLM and onto Strands Decider 2B, AegisOps achieves a **32.6x decision speedup** and eliminates **100% of LLM token spend on high-frequency guardrail checks**.

---

## 2. The Decision Handed to Strands Decider 2B

We handed Strands Decider 2B the most dangerous and critical decision in any autonomous agent: **Pre-Execution Tool Guardrailing & Argument Verification (`#guardrails`)**.

Before any AWS operational tool is invoked (e.g., `scale_service`, `reboot_instance`, `provision_rds_replica`, or `revoke_iam_privileges`), Decider 2B is queried with the incident context and proposed arguments. It evaluates four concurrent typed questions:

```
                  ┌──────────────────────────────────────────────┐
                  │    Incoming Incident Telemetry / Alert       │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │          SYSTEM 1: STRANDS DECIDER 2B        │
                  │   - is_adversarial (Noul: P(attack))         │
                  │   - is_grounded (Noul: P(grounded))          │
                  │   - risk_score (Score: 0.0 - 1.0)            │
                  │   - intervention_choice (Choice: 4 policies) │
                  │                                              │
                  │       Latency: ~47ms | Cost: $0.00000        │
                  └──────┬───────────────────────┬───────────────┘
                         │                       │
           [DENIED / ATTACK]             [APPROVED SAFE]
                         │                       │
                         ▼                       ▼
            ┌────────────────────────┐  ┌────────────────────────┐
            │  Hard Block Tool Call  │  │ Execute AWS Cloud Tool │
            │  (Zero Blast Radius)   │  │ (Scale, Reboot, Block) │
            └────────────┬───────────┘  └────────────┬───────────┘
                         │                           │
                         └───────────────┬───────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │          SYSTEM 2: AMAZON BEDROCK            │
                  │           (Anthropic Claude 3.5)             │
                  │   - Deep Forensic Root-Cause Analysis        │
                  │   - Executive Post-Mortem Synthesis          │
                  │   - Long-Term Infrastructure Runbook         │
                  └──────────────────────────────────────────────┘
```

### The Typed Question Spec
1. `is_adversarial` (`type: noul`): Returns the calibrated probability $P(\text{attack})$ that the proposed call is an adversarial prompt injection or destructive command.
2. `is_grounded` (`type: noul`): Verifies whether parameter IDs (instance IDs, cluster endpoints) exist in the verified CloudWatch telemetry or are LLM hallucinations.
3. `risk_score` (`type: score`): Scores operational blast-radius from `0.0` (read-only/scale) to `1.0` (destructive drop).
4. `intervention_choice` (`type: choice`): Routes to `Proceed`, `Deny`, `Confirm`, or `Guide`.

---

## 3. The Reusable Decision Pattern

Every builder can drop our reusable guardrail handler directly into their Strands or Bedrock agent. The full implementation lives in `reusable_patterns/strands_guardrail_recipe.py`:

```python
from reusable_patterns.strands_guardrail_recipe import StrandsGuardrailRecipe

# 1. Initialize Decider 2B Guardrail Interceptor
guardrail = StrandsGuardrailRecipe(decider_url="http://127.0.0.1:8000/v1/systemone")

# 2. Wire into before_tool_call hook
verdict = guardrail.verify_tool_call(
    tool_name="reboot_instance",
    tool_args={"instance_id": "i-0987abcdef1234567"},
    context="CloudWatch alert: Out-of-memory kernel panic on i-0987abcdef1234567."
)

# 3. Action routing based on calibrated confidence
if verdict.is_safe:
    execute_aws_tool()
else:
    print(f"Blocked by Decider 2B in {verdict.latency_ms:.1f}ms: {verdict.reason}")
```

---

## 4. Empirical Benchmark Results

We evaluated AegisOps across five production incident scenarios using a standardized benchmark harness (`run_benchmarks.py`).

| Scenario Name | Pattern Tag | Decider 2B Latency | Bedrock Latency | Measured Speedup | Fast-Path Token Cost | Calibrated Confidence |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tool Guardrail Verification** | `#guardrails` | **75.4 ms** | 1,550.5 ms | **20.6x** | **$0.0000** | 94% |
| **Adversarial Injection Intercept** | `#guardrails` | **40.7 ms** | 1,550.7 ms | **38.1x** | **$0.0000** | 98% |
| **Traffic Inundation Tool Selection** | `#tool-selection` | **40.3 ms** | 1,550.8 ms | **38.5x** | **$0.0000** | 96% |
| **Operational Severity Policy** | `#policy` | **40.7 ms** | 1,550.4 ms | **38.1x** | **$0.0000** | 92% |
| **RDS Aurora Pool Exhaustion** | `#tool-selection` | **40.6 ms** | 1,550.3 ms | **38.2x** | **$0.0000** | 95% |

### Key Findings:
* **Latency Speedup:** Decider 2B averaged **47.53 ms** compared to Bedrock's **1,550.55 ms** — an overall **32.6x speedup**.
* **Zero Token Cost on Intercepts:** Blocked adversarial prompt injections consumed 0 Bedrock tokens.
* **Projected Scale Savings:** At 10,000 operational checks per day, shifting decision gating to Decider 2B saves **$949.50/month in Bedrock token costs**.

---

## 5. High-Frequency Chaos Alert Storm Evaluation

To prove that Strands Decider 2B excels at repeated, high-frequency decision bursts, we subjected AegisOps to an automated **Chaos Alert Storm** (`run_chaos.py`):
* **50 concurrent production alarms and injection attacks** fired simultaneously.
* **Decider 2B processing duration:** **3.06 seconds** total (~16.4 decisions/sec).
* **Projected Bedrock duration:** **77.5 seconds** (a massive 25.4x latency lag that would breach production SLAs).
* **Security Resilience:** 12 adversarial prompt injections intercepted with 0 data loss.
* **Instant Burst Savings:** **$1.50 in Bedrock token spend saved in 3 seconds**.

---

## 6. Live Interactive Dashboard

To make incident response tangible, AegisOps includes a real-time web command center (`web_dashboard/app.py`). 

Builders and operators can:
1. Select one-click simulated incidents (DDoS, RDS Connection Exhaustion, Prompt Injections, Memory Leaks).
2. Watch real-time System 1 decision pills update in <50ms with calibrated confidence bars.
3. Observe Bedrock asynchronously streaming root-cause forensic post-mortems in markdown.
4. Run live benchmarks comparing latency dials and cost savings in real time.

---

## 6. What I Learned Building with Strands Decider 2B

1. **System 1 Models Complete the Agent Stack:** Trying to use a 70B+ parameter generative LLM to answer binary or multiple-choice questions is like using an excavator to slice bread. Decider 2B's pointer head is laser-focused, deterministic, and fast.
2. **Calibrated Confidence is a Superpower:** Unlike LLM text strings where models express vague certainty ("I think this is safe..."), Decider 2B outputs a mathematical probability. This allowed us to build strict mathematical gate policies: `if confidence < 0.85: ESCALATE_HUMAN`.
3. **Defense in Depth:** Pairing Decider 2B with Amazon Bedrock gives the best of both worlds: unbeatable edge reflex speeds and enterprise-grade generative intelligence.

---

## 7. Try It Yourself

* **Public Repository:** [https://github.com/JeedimetlaCharan704/aegis-ops](https://github.com/JeedimetlaCharan704/aegis-ops)
* **Run CLI Demo:** `python run_demo.py`
* **Run Benchmarks:** `python run_benchmarks.py`
* **Launch Visual Dashboard:** `python web_dashboard/app.py`

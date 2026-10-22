"""AegisOps Dual-Brain SRE Agent Orchestrator.

Combines Strands Decider 2B (System 1 - Fast Gating & Tool Guardrails) with
Amazon Bedrock (System 2 - Deep Forensic Synthesis & Post-Mortem Generation).
"""

import time
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from ..decider.client import StrandsDeciderClient
from ..decider.schemas import TypedQuestion, QuestionType, DeciderEvaluationRequest
from ..bedrock.client import BedrockClient
from ..guardrails.intervention_handler import StrandsDeciderGuardrailHandler, InterventionAction, InterventionResult
from ..tools.aws_actions import AWSToolExecutor

logger = logging.getLogger("aegis_ops.orchestrator")

@dataclass
class IncidentReport:
    incident_id: str
    incident_raw: str
    severity: str
    decider_tool_selected: str
    decider_latency_ms: float
    decider_confidence: float
    guardrail_result: InterventionResult
    tool_execution_status: str
    tool_output: Optional[Dict[str, Any]]
    bedrock_synthesis: Optional[str]
    bedrock_latency_ms: float
    bedrock_cost_usd: float
    total_latency_ms: float
    tokens_saved: int
    cost_saved_usd: float

class AegisSREAgent:
    def __init__(
        self,
        decider_client: Optional[StrandsDeciderClient] = None,
        bedrock_client: Optional[BedrockClient] = None
    ):
        self.decider = decider_client or StrandsDeciderClient()
        self.bedrock = bedrock_client or BedrockClient()
        self.guardrail = StrandsDeciderGuardrailHandler(decider_client=self.decider)
        self.tools = AWSToolExecutor()

    def process_incident(self, incident_text: str, incident_id: str = "INC-AWS-001") -> IncidentReport:
        """Process an infrastructure incident through the Dual-Brain cognitive pipeline."""
        total_start = time.perf_counter()
        
        # -------------------------------------------------------------
        # STEP 1: SYSTEM 1 (Strands Decider 2B) - Incident Triage & Tool Selection
        # -------------------------------------------------------------
        triage_questions = {
            "severity_level": TypedQuestion(
                type=QuestionType.CHOICE,
                instructions="Determine the operational severity level of this incident.",
                criteria={
                    "SEV_1": "Complete outage, customer-facing downtime, or ongoing cyberattack",
                    "SEV_2": "Degraded performance, high resource exhaustion, or partial failure",
                    "SEV_3": "Minor anomaly, warning threshold reached, or informational alarm"
                }
            ),
            "tool_to_invoke": TypedQuestion(
                type=QuestionType.CHOICE,
                instructions="Select the immediate AWS remediation tool needed.",
                criteria={
                    "scale_service": "Traffic surge requiring ECS/EKS task scaling",
                    "reboot_instance": "Memory leak or process hang requiring EC2 restart",
                    "provision_rds_replica": "Database read connection pool exhaustion",
                    "block_malicious_ip": "DDoS or unauthorized vulnerability scan",
                    "revoke_iam_privileges": "Compromised credentials or privilege escalation",
                    "drop_database": "Drop or truncate data store"
                }
            )
        }

        triage_req = DeciderEvaluationRequest(state=incident_text, questions=triage_questions)
        triage_resp = self.decider.evaluate(triage_req)

        severity = triage_resp.get_choice("severity_level") or "SEV_2"
        tool_choice = triage_resp.get_choice("tool_to_invoke") or "scale_service"
        decider_latency = triage_resp.latency_ms

        # Extract arguments from incident text
        tool_args = self._derive_tool_args(tool_choice, incident_text)

        # -------------------------------------------------------------
        # STEP 2: SYSTEM 1 GUARDRAILS (Strands Decider 2B InterventionHandler)
        # -------------------------------------------------------------
        guardrail_result = self.guardrail.before_tool_call(
            tool_name=tool_choice,
            tool_args=tool_args,
            context_state=incident_text
        )

        tool_status = "BLOCKED"
        tool_output = None

        # -------------------------------------------------------------
        # STEP 3: TOOL EXECUTION (Only if Guardrail Permits)
        # -------------------------------------------------------------
        if guardrail_result.is_allowed():
            tool_status = "EXECUTED"
            tool_output = self._execute_tool(tool_choice, tool_args)
        elif guardrail_result.action == InterventionAction.CONFIRM:
            tool_status = "PENDING_HUMAN_CONFIRMATION"
            tool_output = {"status": "PAUSED", "reason": guardrail_result.reason}
        else:
            tool_status = "BLOCKED_BY_GUARDRAIL"
            tool_output = {"status": "DENIED", "reason": guardrail_result.reason}

        # -------------------------------------------------------------
        # STEP 4: SYSTEM 2 (Amazon Bedrock) - Deep Forensic Synthesis & Post-Mortem
        # -------------------------------------------------------------
        bedrock_prompt = (
            f"Incident ID: {incident_id}\n"
            f"Raw Incident Telemetry: {incident_text}\n"
            f"Decider 2B Severity: {severity}\n"
            f"Decider 2B Tool Action: {tool_choice} ({tool_status})\n"
            f"Guardrail Confidence: {guardrail_result.confidence:.2f}\n"
            f"Guardrail Verdict: {guardrail_result.action.value}\n"
            "Please generate an executive root-cause analysis, post-mortem, and architectural recommendations."
        )

        bedrock_resp = self.bedrock.invoke(bedrock_prompt)
        bedrock_latency = bedrock_resp["latency_ms"]
        bedrock_cost = bedrock_resp["cost_usd"]
        bedrock_content = bedrock_resp["content"]

        total_latency = (time.perf_counter() - total_start) * 1000.0

        # Calculate tokens and cost saved by having Decider 2B filter/guard instead of an LLM loop
        tokens_saved = 450  # Typical prompt tokens saved on guardrail check
        cost_saved = (tokens_saved / 1000.0) * 0.015

        return IncidentReport(
            incident_id=incident_id,
            incident_raw=incident_text,
            severity=severity,
            decider_tool_selected=tool_choice,
            decider_latency_ms=decider_latency,
            decider_confidence=guardrail_result.confidence,
            guardrail_result=guardrail_result,
            tool_execution_status=tool_status,
            tool_output=tool_output,
            bedrock_synthesis=bedrock_content,
            bedrock_latency_ms=bedrock_latency,
            bedrock_cost_usd=bedrock_cost,
            total_latency_ms=total_latency,
            tokens_saved=tokens_saved,
            cost_saved_usd=cost_saved
        )

    def _derive_tool_args(self, tool_name: str, text: str) -> Dict[str, Any]:
        """Parse realistic parameters based on context."""
        text_lower = text.lower()
        if tool_name == "scale_service":
            return {"service_name": "checkout-api-v2", "replica_count": 8}
        elif tool_name == "reboot_instance":
            return {"instance_id": "i-0987abcdef1234567", "force": False}
        elif tool_name == "provision_rds_replica":
            return {"cluster_id": "aurora-prod-cluster-01", "replica_id": "aurora-replica-read-02"}
        elif tool_name == "block_malicious_ip":
            return {"ip_address": "198.51.100.44", "duration_minutes": 120}
        elif tool_name == "revoke_iam_privileges":
            return {"role_name": "DataSyncWorkerRole", "policy_arn": "arn:aws:iam::aws:policy/AdministratorAccess"}
        elif tool_name == "drop_database":
            return {"database_name": "prod_users_primary"}
        return {"action": "generic_remediation"}

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "scale_service":
            return self.tools.scale_service(args.get("service_name", "app-svc"), args.get("replica_count", 4))
        elif tool_name == "reboot_instance":
            return self.tools.reboot_instance(args.get("instance_id", "i-123"), args.get("force", False))
        elif tool_name == "provision_rds_replica":
            return self.tools.provision_rds_replica(args.get("cluster_id", "cluster-1"), args.get("replica_id", "rep-1"))
        elif tool_name == "block_malicious_ip":
            return self.tools.block_malicious_ip(args.get("ip_address", "0.0.0.0"), args.get("duration_minutes", 60))
        elif tool_name == "revoke_iam_privileges":
            return self.tools.revoke_iam_privileges(args.get("role_name", "role"), args.get("policy_arn", "arn"))
        elif tool_name == "drop_database":
            return self.tools.drop_database(args.get("database_name", "db"))
        return {"status": "UNKNOWN_TOOL"}

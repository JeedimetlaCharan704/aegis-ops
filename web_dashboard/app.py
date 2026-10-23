"""Flask Web Dashboard for AegisOps Autonomous SRE Agent.

Provides an interactive GUI for judges and developers to simulate incidents,
observe real-time Strands Decider 2B guardrail intercepts, and view Amazon Bedrock
forensic post-mortems.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os

# Ensure parent directory is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")
STATIC_DIR = os.path.join(CURRENT_DIR, "static")

from aegis_ops.agent.orchestrator import AegisSREAgent
from aegis_ops.agent.chaos_engine import ChaosAlertStormEngine
from aegis_ops.benchmarks.benchmark_runner import DeciderBenchmarkRunner

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)

# Vercel WSGI Proxy Middleware to restore original request URI
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # 1. Check for __path parameter passed from vercel.json rewrite
        query = environ.get("QUERY_STRING", "")
        if "__path=" in query:
            for part in query.split("&"):
                if part.startswith("__path="):
                    p = part.split("=", 1)[1]
                    if p:
                        environ["PATH_INFO"] = "/" + p.lstrip("/")
                    else:
                        environ["PATH_INFO"] = "/"
                    break
        else:
            orig_path = environ.get("HTTP_X_FORWARDED_URI") or environ.get("HTTP_X_VERCEL_FORWARDED_PATH")
            if orig_path:
                if "?" in orig_path:
                    orig_path = orig_path.split("?")[0]
                environ["PATH_INFO"] = orig_path
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

agent = AegisSREAgent()
benchmark_runner = DeciderBenchmarkRunner()
chaos_engine = ChaosAlertStormEngine(agent=agent)

@app.route("/")
@app.route("/api")
@app.route("/api/index", methods=["GET", "POST"])
@app.route("/index")
def index():
    return render_template("index.html")
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        orig = (
            request.environ.get("HTTP_X_FORWARDED_URI") or 
            request.environ.get("HTTP_X_VERCEL_FORWARDED_PATH") or 
            request.headers.get("x-matched-path") or 
            request.path or ""
        )
        if "incident_text" in data or "simulate" in orig:
            return simulate_incident()
        elif "count" in data or "chaos" in orig:
            return trigger_chaos()
        elif "benchmark" in orig:
            return run_benchmark()
    return render_template("index.html")

@app.route("/api/debug", methods=["GET", "POST"])
@app.route("/debug", methods=["GET", "POST"])
def debug_env():
    return jsonify({
        "path_info": request.environ.get("PATH_INFO"),
        "x_forwarded_uri": request.environ.get("HTTP_X_FORWARDED_URI"),
        "x_vercel_forwarded_path": request.environ.get("HTTP_X_VERCEL_FORWARDED_PATH"),
        "x_matched_path": request.headers.get("x-matched-path"),
        "headers": dict(request.headers),
        "method": request.method
    })

@app.route("/api/simulate", methods=["POST"])
@app.route("/simulate", methods=["POST"])
def simulate_incident():
    """Trigger incident processing through the Dual-Brain SRE Agent."""
    data = request.json or {}
    incident_text = data.get("incident_text", "High CPU load on worker node.")
    incident_id = data.get("incident_id", "INC-LIVE-001")

    report = agent.process_incident(incident_text, incident_id=incident_id)

    return jsonify({
        "incident_id": report.incident_id,
        "incident_raw": report.incident_raw,
        "severity": report.severity,
        "decider_tool": report.decider_tool_selected,
        "decider_latency_ms": round(report.decider_latency_ms, 1),
        "decider_confidence": round(report.decider_confidence, 2),
        "guardrail_action": report.guardrail_result.action.value,
        "guardrail_reason": report.guardrail_result.reason,
        "is_adversarial": report.guardrail_result.is_adversarial,
        "tool_status": report.tool_execution_status,
        "tool_output": report.tool_output,
        "bedrock_synthesis": report.bedrock_synthesis,
        "bedrock_latency_ms": round(report.bedrock_latency_ms, 1),
        "bedrock_cost_usd": report.bedrock_cost_usd,
        "total_latency_ms": round(report.total_latency_ms, 1),
        "tokens_saved": report.tokens_saved,
        "cost_saved_usd": round(report.cost_saved_usd, 4),
        "speedup_factor": round(report.bedrock_latency_ms / max(1.0, report.decider_latency_ms), 1)
    })

@app.route("/api/chaos", methods=["POST"])
@app.route("/chaos", methods=["POST"])
def trigger_chaos():
    """Execute high-frequency alert storm through Strands Decider 2B."""
    data = request.json or {}
    count = int(data.get("count", 50))
    burst_data = chaos_engine.run_burst(count=count)
    return jsonify(burst_data)

@app.route("/api/benchmark", methods=["POST"])
@app.route("/benchmark", methods=["POST"])
def run_benchmark():
    """Run full benchmark suite comparing Decider 2B vs Bedrock."""
    benchmark_data = benchmark_runner.run_suite(iterations=1)
    return jsonify(benchmark_data)

@app.route("/api/health")
@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "AegisOps Decider Co-Pilot"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

import os
import time
import uuid
import litellm
from typing import List, Dict, Optional

from fastapi import FastAPI, Header
from pydantic import BaseModel

from mcp.controller import is_allowed
from agents.agent import run_agent


APP_NAME = "ai-security-guardrails-demo"
DEFAULT_MODEL = os.getenv("LITELLM_DEFAULT_MODEL", "gpt-4o-mini")

app = FastAPI(title=APP_NAME)


class ChatRequest(BaseModel):
    # ChatGPT-style messages
    messages: List[Dict[str, str]]
    # Optional: if the user wants to trigger an "agent action"
    use_agent: Optional[bool] = False
    # Optional: requested action name for MCP gating (demo purpose)
    action: Optional[str] = None
    # Optional: agent name
    agent_name: Optional[str] = "safe_agent"


def _audit(event: Dict):
    # Minimal audit log to stdout (easy to demo live)
    print("[AUDIT] " + " ".join([f"{k}={v}" for k, v in event.items()]))


@app.get("/healthz")
def healthz():
    return {"ok": True, "service": APP_NAME}


MCP_POLICY = {
    "safe_agent": [
        "read_internal_data",
        "analyze_logs"
        ]
    }

def is_allowed(agent_name: str, action: str) -> bool:
    return action in MCP_POLICY.get(agent_name, [])

@app.post("/v1/chat")
def chat(req: ChatRequest, x_user: Optional[str] = Header(default="unknown")):
    request_id = str(uuid.uuid4())
    start = time.time()

    # If agent usage requested, enforce MCP policy first
    if req.use_agent:
        action = req.action or "read_internal_data"
        allowed = is_allowed(req.agent_name or "safe_agent", action)
        if not allowed:
            _audit({
                "request_id": request_id,
                "user": x_user,
                "decision": "deny",
                "reason": "mcp_policy",
                "agent": req.agent_name,
                "action": action
            })
            return {
                "request_id": request_id,
                "decision": "deny",
                "reason": f"MCP denied action '{action}' for agent '{req.agent_name}'"
            }

        # Run agent (controlled tool usage)
        agent_output = run_agent(req.messages, action=action)
        latency = round(time.time() - start, 3)
        _audit({
            "request_id": request_id,
            "user": x_user,
            "decision": "allow",
            "path": "agent",
            "agent": req.agent_name,
            "action": action,
            "latency_s": latency
        })
        return {"request_id": request_id, "path": "agent", "output": agent_output}

    # Normal chat via LiteLLM
    response = litellm.completion(
        model=DEFAULT_MODEL,
        messages=req.messages,
    )

    latency = round(time.time() - start, 3)
    _audit({
        "request_id": request_id,
        "user": x_user,
        "decision": "allow",
        "path": "chat",
        "model": DEFAULT_MODEL,
        "latency_s": latency
    })

    return {
        "request_id": request_id,
        "path": "chat",
        "model": DEFAULT_MODEL,
        "reply": response.choices[0].message["content"],
    }

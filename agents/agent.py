from typing import List, Dict
from litellm import completion

from agents.tools import read_internal_data

# -----------------------------------------------------------------------------
# Guardrails (simple, demo-friendly)
# -----------------------------------------------------------------------------
# NOTE:
# - This is intentionally lightweight so we can demo the idea without a heavy policy engine.
# - In production, this would be replaced by: Model Armor / DLP / OPA policy, etc.
# -----------------------------------------------------------------------------

def violates_bias_policy(text: str) -> bool:
    """Very simple bias/discrimination detector (keyword-based).
    Purpose: show "application-layer enforcement" in the agent before we return output.
    """
    banned_patterns = [
        "based on race",
        "racial profiling",
        "treat customers differently",
        "charge more because",
        "avoid certain groups",
        "discriminate",
    ]
    t = (text or "").lower()
    return any(p in t for p in banned_patterns)


def run_agent(messages: List[Dict[str, str]], action: str = "read_internal_data") -> str:
    """Minimal agent: calls a tool, then uses the model to format a helpful answer."""
    tool_result = ""
    if action == "read_internal_data":
        tool_result = read_internal_data()
    else:
        tool_result = f"Unknown action: {action}"

    # Add tool result to the conversation context
    augmented = messages + [
        {"role": "system", "content": "You are a helpful assistant. Keep answers concise."},
        {"role": "system", "content": f"Tool result:\n{tool_result}"},
    ]

    # Model call (through LiteLLM)
    resp = completion(
        model="gpt-4o-mini",
        messages=augmented,
    )

    final_output = resp.choices[0].message["content"]

    # Application-layer guardrail enforcement (demo)
if violates_bias_policy(final_output):
    print("🚨 GUARDRAIL TRIGGERED: Bias policy violation")
    return {
        "guardrail_triggered": True,
        "reason": "Bias / discrimination policy",
        "message": (
            "This request was blocked by AI security guardrails. "
            "I can help with a fair and policy-compliant alternative."
        ),
    }
        return (
            "I can’t help with requests that involve discrimination or biased treatment. "
            "I can help with fair, policy-compliant alternatives instead."
        )

    return final_output

# Day 2 — LiteLLM Proxy Layer (Enterprise Control Point)

## Overview

Day 2 extends the Day-1 secure agent foundation by introducing a **LiteLLM proxy layer**.

In enterprise AI systems, direct model access becomes unmanageable quickly:
- no standardized interface
- inconsistent logging across apps
- difficult cost/routing control
- hard to enforce centralized security policies

A proxy acts as the **single entry point** for model calls — enabling governance, observability, and future policy enforcement.

---

## Why a Proxy Layer Matters

A proxy enables:

- **Standard API interface** (OpenAI-compatible `/v1/chat/completions`)
- **Centralized routing** (choose models by policy/cost/env)
- **Audit logging** (who called what, when, and how often)
- **Security hooks** (where MCP policy enforcement plugs in)
- **Future CI/CD gates** (Promptfoo/Garak/PyRIT triggered before onboarding)

Think of it as the **traffic control tower** for LLM usage.

---

## Architecture (Day 2)

User  
↓  
Agent  
↓  
LiteLLM Proxy (central entry point)  
↓  
Model Provider (OpenAI / internal gateway / ModelHub)  
↓  
Response  
↓  
Guardrail enforcement (Day 1)  
↓  
Final response  

---

## Files Added (Day 2)

```
litellm_proxy/
  proxy_client.py
  litellm_proxy.env.example
  README.md
```

---

## How to Run

1) Set env variables (Windows PowerShell / CMD):

CMD:
```
set LITELLM_BASE_URL=http://localhost:4000
set LITELLM_API_KEY=dev-key
```

2) Install dependencies:
```
pip install -r requirements.txt
```

3) Run:
```
python litellm_proxy\proxy_client.py
```

Expected output includes an audit log line:
```
[AUDIT] {"event":"litellm_proxy_call","url":"http://localhost:4000/v1/chat/completions","model":"gpt-4o-mini","latency_ms":412,"status_code":200}
```

---

## What This Demonstrates

✔ Centralized LLM access via proxy  
✔ OpenAI-compatible routing pattern  
✔ Audit-style logging for enterprise tracking  
✔ Clean foundation for MCP policy control  

---

## What Comes Next (Day 3)

Day 3 adds the **MCP policy controller**:
- structured allow/deny decisions
- risk scoring (0–100)
- standardized security JSON reports

Then we connect:
Promptfoo → regression tests  
Garak → vulnerability scanning  
PyRIT → multi-turn red teaming  

---

## Author

Nagadeep — AI Security & DevSecOps Engineer

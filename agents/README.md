# AI Security Guardrails Demo (LiteLLM + Promptfoo + Agents + MCP)

This is a **minimal but real** platform-style repo:
- **LiteLLM** for a controlled AI access layer
- **Promptfoo** for evaluation gating (before release)
- **Agents** for tool-using workflows
- **MCP** for centralized policy over agent actions

## 0) Prereqs
- Python 3.10+ on your VM
- Node 18+ (only for Promptfoo)

## 1) Set your OpenAI key (never hardcode keys)
```bash
export OPENAI_API_KEY="sk-..."
```

## 2) Install Python deps (recommended: venv)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Run the Guardrails API (LiteLLM-backed)
```bash
uvicorn litellm_proxy.proxy:app --host 0.0.0.0 --port 4000
```

### Quick API test (ChatGPT-style messages)
```bash
curl -s -X POST "http://127.0.0.1:4000/v1/chat" \
  -H "Content-Type: application/json" \
  -H "X-User: naga" \
  -d '{"messages":[{"role":"user","content":"Explain zero trust in one line"}]}' | python3 -m json.tool
```

### Agent test (MCP-gated)
```bash
curl -s -X POST "http://127.0.0.1:4000/v1/chat" \
  -H "Content-Type: application/json" \
  -H "X-User: naga" \
  -d '{"messages":[{"role":"user","content":"Summarize internal winsurf logs and recommend next step"}],"use_agent":true,"agent_name":"safe_agent","action":"read_internal_data"}' | python3 -m json.tool
```

## 4) Run the "Ask Anything" bar (simple web UI)
In a second terminal:
```bash
export GUARDRAILS_API_URL="http://127.0.0.1:4000/v1/chat"
uvicorn ui.app:app --host 0.0.0.0 --port 8080
```

Open:
- Local: http://127.0.0.1:8080
- From your laptop: http://<VM_IP>:8080

## 5) Run Promptfoo (evaluation gate)
```bash
cd evaluations
npx promptfoo@latest eval
```

## What to demo (simple story)
1) Ask Anything bar -> chat response (shows "feels like ChatGPT")
2) Show audit logs in the API terminal (request_id, user, latency)
3) Check "Use Agent" -> shows MCP policy + tool-based answer
4) Run promptfoo eval -> show pass/fail and explain "this gates releases"


## Demo
See `DEMO_RUNBOOK.md` for the exact steps to run API + Promptfoo + Web View.

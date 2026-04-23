# my-langgraph-agent (Ollama variant)

A 2-node LangGraph agent running entirely on your local machine via
[Ollama](https://ollama.com). No API key. No cloud.

## Prerequisites

1. **Install Ollama** — https://ollama.com/download
2. **Pull a model** — open a terminal and run one of:
   ```bash
   ollama pull llama3.2:3b    # small, works on most laptops
   ollama pull llama3.1:8b    # better, needs ~8GB RAM
   ollama pull qwen2.5:7b     # strong instruction-follower
   ```
3. **Verify Ollama is running** — the service auto-starts after install.
   Test with:
   ```bash
   ollama run llama3.2:3b "hi"
   ```

## Project setup

```bash
cd my-langgraph-agent-ollama

# Virtual env
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate          # Windows PowerShell

# Install deps
pip install -r requirements.txt
pip install -e .

# Configure which model to use (optional — defaults are sensible)
cp .env.example .env
# Edit .env if you want to change the model
```

## Run

```bash
python scripts/run_agent.py "Explain async/await in Python"
```

First run will be slower — Ollama loads the model into RAM. Subsequent
runs are fast because the model stays resident.



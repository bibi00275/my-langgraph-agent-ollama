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

## Run tests (offline, no Ollama needed)

```bash
pytest
```

Tests use a `FakeLLM` so they run in milliseconds with zero dependencies
on Ollama or any network.



**"Connection refused" on localhost:11434**
Ollama isn't running. On macOS, check the menu bar. On Linux, run
`systemctl status ollama`. On Windows, re-open the Ollama app.

**"Model not found"**
You haven't pulled it yet. Run `ollama pull <model-name>` (must match
the `AGENT_MODEL` value in `.env`).

**Slow responses**
Normal for local inference, especially the first call after startup.
Try a smaller model like `llama3.2:3b` if your machine is struggling.
Check Activity Monitor / Task Manager — if RAM is pegged, use a smaller model.

**Output format is worse than Claude**
Expected — small local models follow complex instructions less reliably.
Mitigations: use a bigger model, simplify prompts, or add output validation
with retries in the analyzer.

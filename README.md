# MaintainerLens

**AI-assisted GitHub issue triage for open-source maintainers.**

MaintainerLens turns incomplete bug reports into structured triage notes. It helps maintainers identify missing diagnostic details, review possible impact, and prepare a useful response without handing control of the repository to an automated agent.

## What it does

- Accepts a public GitHub issue URL or a pasted issue report.
- Retrieves public issue details through the GitHub REST API.
- Checks for commonly missing details such as reproduction steps, logs, environment, and expected behaviour.
- Uses a locally running Ollama model for AI-assisted analysis.
- Falls back to a clearly labelled deterministic checklist when model inference is unavailable.
- Produces a Markdown report with evidence, missing information, a priority suggestion, and a draft maintainer reply.
- Lets maintainers download the report as Markdown.

**Human-in-the-loop by design:** MaintainerLens does not post comments, change labels, or modify repositories. Priority suggestions are prompts for human review, not authoritative severity decisions.

## Technology

- Python 3.11+
- Streamlit
- GitHub REST API
- Ollama-compatible local model endpoint

## Requirements

- Python 3.11 or newer
- Internet access to retrieve public GitHub issues
- Ollama installed and running for AI-assisted analysis
- A model available to the configured Ollama instance

The application can still produce a rule-based report when Ollama is unavailable.

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/amansharmas7/MaintainerLens.git
cd MaintainerLens
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the app

```bash
python -m streamlit run streamlit_app.py
```

Open the local address printed by Streamlit (normally http://localhost:8501).

## Configure Ollama

The sidebar lets you set the Ollama base URL and model name. Defaults can also be configured with environment variables:

- `OLLAMA_URL` — Ollama API base URL (default: `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` — model name to send to Ollama (default: `gemma4:e2b`)

Make sure the selected model is available to the Ollama instance. You can use a local model or an Ollama-supported cloud model, depending on your account and configuration.

## Use it

1. Paste a public GitHub issue URL, or paste the issue description.
2. Choose the Ollama base URL and model in the sidebar.
3. Select **Analyze issue**.
4. Review the evidence, missing-information checklist, and draft reply.
5. Download the report as a Markdown file.

## Project structure

```text
.
├── streamlit_app.py
├── requirements.txt
├── docs/
│   ├── maintainerlens-architecture.md
│   └── maintainerlens-demo.png
└── .github/
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

## Development checks

A lightweight GitHub Actions workflow compiles the Streamlit application on pushes and pull requests. Run the same syntax check locally:

```bash
python -m compileall -q streamlit_app.py
```

## Responsible use and limitations

- Only public GitHub issue URLs are supported by the current issue fetcher.
- Unauthenticated GitHub API requests are subject to GitHub's public rate limits.
- The fallback report is keyword-based and must not be treated as an AI diagnosis.
- Model output can be incomplete or incorrect; verify suggestions before acting on them.
- Do not paste passwords, access tokens, private issue contents, personal data, or other secrets.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

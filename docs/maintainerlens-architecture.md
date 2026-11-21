# MaintainerLens architecture

## Overview

MaintainerLens separates its Streamlit presentation layer from issue retrieval, local-model inference and fallback report generation.

## Components

### Streamlit interface — `streamlit_app.py`

Collects an issue URL or pasted report, exposes Ollama endpoint/model settings, manages the current result in Streamlit session state, and renders/downloads the Markdown report.

### Core module — `maintainerlens/core.py`

- `parse_github_issue_url`: validates canonical HTTPS GitHub issue URLs.
- `fetch_github_issue`: retrieves public issue metadata and normalizes it into a stable internal record.
- `run_local_model`: calls an Ollama-compatible `/api/generate` endpoint and validates the response.
- `build_fallback_report`: produces a deterministic missing-information checklist when model inference is unavailable.

The core module does not import Streamlit, allowing tests to exercise its behaviour without starting a UI server.

### Test suite — `tests/test_core.py`

Covers canonical and rejected issue URLs, normalized GitHub response records, rejection of pull-request payloads, fallback report contents, invalid model endpoints, and the Ollama request/response contract.

## Data flow

1. The user supplies a public GitHub issue URL or a pasted issue report.
2. URL input is validated before the GitHub API request.
3. GitHub data is normalized into a compact issue object.
4. MaintainerLens attempts local model inference.
5. If model inference fails, a deterministic fallback report is generated.
6. The result is shown for human review and can be downloaded as Markdown.

## Trust boundaries

- Issue descriptions and model responses are treated as untrusted content.
- The model is instructed not to follow instructions embedded in issue text.
- No GitHub write token is configured or used; the application does not post comments or modify issues.
- The model endpoint is configurable, so deployments exposed to untrusted users should restrict outbound network access and add application authentication.
- Fallback priority flags are keyword-based and are not security or severity assessments.

## Extension points

Potential future improvements include structured output validation, GitHub App authentication with narrowly scoped permissions, configurable issue-quality checks, repository-specific templates, and an optional maintainer approval workflow.

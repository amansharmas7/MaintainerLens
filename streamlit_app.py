import json
import os
from urllib.error import HTTPError, URLError

import streamlit as st

from maintainerlens.core import (
    build_fallback_report,
    fetch_github_issue,
    format_ai_report,
    run_local_model,
    validate_issue_text,
)

st.set_page_config(
    page_title="MaintainerLens",
    page_icon="🔎",
    layout="wide",
)

DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:e2b")
DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 1200px;}
    .hero {
        padding: 1.4rem 1.6rem; border-radius: 16px;
        background: linear-gradient(120deg, #14213d, #243b64);
        border: 1px solid #415477; margin-bottom: 1.3rem;
    }
    .eyebrow {letter-spacing: 2px; font-size: .75rem; color: #a9c6ff;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">OPEN-SOURCE AI · HACKTOBERFEST</div>
      <h1>🔎 MaintainerLens</h1>
      <p>Turn unclear GitHub issues into actionable, evidence-aware
      maintainer responses.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Human-in-the-loop issue triage. The application does not modify "
    "repositories or post replies to GitHub."
)

with st.sidebar:
    st.header("AI configuration")
    ollama_url = st.text_input("Ollama base URL", value=DEFAULT_OLLAMA_URL)
    model_name = st.text_input("Local model name", value=DEFAULT_MODEL)
    st.info(
        "AI analysis requires Ollama to be installed, running, and "
        "configured with the selected model."
    )
    st.caption("Public GitHub issues only. Do not paste secrets or tokens.")

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("1. Provide an issue")
    issue_url = st.text_input(
        "Public GitHub issue URL",
        placeholder="https://github.com/owner/repo/issues/123",
    )
    issue_text = st.text_area(
        "Or paste issue details",
        placeholder=(
            "Describe the problem, reproduction steps, error messages, "
            "and expected behavior..."
        ),
        height=190,
    )
    analyze = st.button("Analyze issue →", type="primary", use_container_width=True)
    st.caption(
        "If a GitHub URL is provided, the app retrieves the issue through "
        "the GitHub REST API. Otherwise, it analyzes the pasted text."
    )

with right:
    st.subheader("2. Triage report")
    if analyze:
        try:
            if issue_url.strip():
                with st.spinner("Retrieving issue from GitHub..."):
                    issue = fetch_github_issue(issue_url)
            else:
                cleaned_text = validate_issue_text(issue_text)
                issue = {
                    "title": "Pasted issue report",
                    "body": cleaned_text,
                    "url": "Pasted by user",
                    "state": "unknown",
                    "labels": [],
                    "comments": "Not supplied",
                    "repository": "Not supplied",
                    "author": "Not supplied",
                }

            ai_error = None
            with st.spinner("Attempting local model analysis..."):
                try:
                    model_report = run_local_model(issue, ollama_url, model_name)
                    report = format_ai_report(model_report, model_name)
                    mode = f"AI-assisted (local Ollama: {model_name})"
                except Exception as exc:
                    ai_error = str(exc)
                    report = build_fallback_report(issue)
                    mode = "Rule-based fallback (not AI)"

            st.session_state["maintainerlens_result"] = {
                "issue": issue,
                "report": report,
                "mode": mode,
                "ai_error": ai_error,
            }

        except HTTPError as exc:
            message = (
                "Issue not found or not public."
                if exc.code == 404
                else f"GitHub returned HTTP {exc.code}."
            )
            st.error(message)
        except (URLError, TimeoutError) as exc:
            st.error(
                "Could not reach GitHub. Check your internet connection. "
                f"Details: {exc}"
            )
        except (ValueError, json.JSONDecodeError) as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")

    result = st.session_state.get("maintainerlens_result")
    if result:
        st.success(f"Analysis mode: {result['mode']}")
        if result["ai_error"]:
            with st.expander("Why wasn't the AI model used?"):
                st.write(result["ai_error"])
                st.write(
                    "The report below uses a deterministic, rule-based checklist, "
                    "not an AI model."
                )
        st.markdown(result["report"])
        st.download_button(
            "Download triage report",
            data=result["report"],
            file_name="maintainerlens-triage.md",
            mime="text/markdown",
            use_container_width=True,
        )
        with st.expander("Retrieved issue data"):
            st.json(result["issue"])
    else:
        st.info(
            "Your summary, missing-information checklist, priority suggestion, "
            "and reply draft will appear here."
        )

st.divider()
st.caption(
    "MaintainerLens · Open source · Evidence over guesses · "
    "All priority suggestions require maintainer judgment."
)

# Graph Report - MaintainerLens  (2026-10-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 14 nodes · 16 edges · 4 communities (0 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a1443275`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- json
- fetch_github_issue
- build_fallback_report

## God Nodes (most connected - your core abstractions)
1. `fetch_github_issue()` - 4 edges
2. `run_local_model()` - 3 edges
3. `build_fallback_report()` - 2 edges
4. `Ask a locally running Ollama model to analyze an issue.` - 1 edges
5. `Retrieve a public GitHub issue using the GitHub REST API.` - 1 edges
6. `Produce a rule-based checklist, not an AI-generated diagnosis.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `fetch_github_issue()` --calls--> `json`  [EXTRACTED]
  streamlit_app.py →   _Bridges community 2 → community 1_

## Import Cycles
- None detected.

## Communities (4 total, 4 thin omitted)

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `fetch_github_issue()` connect `fetch_github_issue` to `streamlit_app.py`, `json`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `run_local_model()` connect `json` to `streamlit_app.py`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `build_fallback_report()` connect `build_fallback_report` to `streamlit_app.py`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
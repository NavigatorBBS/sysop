# Copilot Instructions

## Build, test, and lint commands

Use the `src/` layout and install in editable mode before running checks:

```bash
pip install -e ".[dev]"
```

Run the full test suite:

```bash
python -m pytest tests -v
```

Run a single test file:

```bash
python -m pytest tests/test_copilot_integration.py -v
```

Run a single test case:

```bash
python -m pytest tests/test_copilot_integration.py::TestCopilotSDKIntegration::test_markdown_response -v
```

If you intentionally want the live Copilot integration test, set `GITHUB_COPILOT_PAT` first and run:

```bash
python -m pytest tests/test_copilot_integration.py::TestCopilotSDKIntegration::test_live_chat -v
```

Use the GitHub Actions lint commands as the source of truth for CI-compatible checks:

```bash
python -m black --check src tests examples
python -m isort --check-only src tests examples
python -m flake8 src tests examples --max-line-length=100 --extend-ignore=E203,W503
```

For local formatting, the contributor docs use:

```bash
python -m black src tests examples
python -m isort src tests examples
```

## High-level architecture

The package is centered on `src/sysop/chatbot_agent.py`. `NotebookChatAgent` wraps `copilot.CopilotClient`, lazily starts the client and session on first use, and exposes the public workflow methods: `chat()`, `analyze_code()`, `suggest_notebook_improvements()`, `get_messages()`, `clear_history()`, and `cleanup()`. The actual request/response path is event-driven: `_send_and_wait()` subscribes to Copilot session events, collects the `assistant.message` payload, and completes when the session becomes idle.

There are two entry points built on top of that same agent. `src/sysop/cli.py` is a thin terminal harness: it loads `.env` from the repository root, constructs `NotebookChatAgent`, and forces `chat(..., as_markdown=False)` so the CLI prints plain text. `src/sysop/jupyter_extension.py` is the IPython/Jupyter integration layer used by `%load_ext sysop`; it reads `GITHUB_COPILOT_PAT` from the environment, creates the same agent, injects `agent`, `display`, and `Markdown` into `ipython.user_ns`, and surfaces readiness/errors through rendered Markdown.

`src/sysop/__init__.py` re-exports both the core agent types and the IPython extension hooks, so package imports and notebook extension loading both route through the same small surface area. The test suite in `tests/test_copilot_integration.py` is a mix of smoke tests and an optional live integration test gated by `GITHUB_COPILOT_PAT`.

## Key conventions

- Keep tool registration and plugin setup ahead of first use. `NotebookChatAgent` only adds `self.tools` into the session config during lazy session creation, and `add_plugin()` refuses late registration once a session exists.
- Preserve the notebook/plain-text split. `chat()` returns `MarkdownResponse` by default so notebook cells auto-render Markdown, while the CLI explicitly opts out with `as_markdown=False`.
- Expect lazy session lifecycle behavior. A new session is created on first chat, `clear_history()` destroys the current session so the next call starts fresh, and `cleanup()` destroys the session and stops the Copilot client.
- Use `GITHUB_COPILOT_PAT` as the single credential source. The CLI auto-loads it from the repo-root `.env`; Jupyter extension usage expects it to already be present in the environment.
- Follow the repo’s documented Python style: type hints on public APIs, Google-style docstrings, and a 100-character line length enforced by Black/isort/Flake8 settings.
- The current CLI entry point is the installed `sysop` console script from `pyproject.toml` (`sysop = sysop.cli:run`). `setup.ps1` still references `main.py`, so prefer the console script or `python -m sysop.cli` when updating or validating CLI behavior.

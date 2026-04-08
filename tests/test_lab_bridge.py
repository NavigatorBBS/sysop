from types import SimpleNamespace

import pytest

from sysop.chatbot_agent import build_notebook_cell_prompt
from sysop.lab_bridge import (
    PUBLIC_BRIDGE_NAME,
    SysopLabBridge,
    get_or_create_lab_bridge,
    handle_lab_request,
)


class FakeAgent:
    """Simple async agent double for bridge tests."""

    def __init__(self):
        self.calls = []

    async def chat(self, message, as_markdown=True):
        self.calls.append(("chat", message, as_markdown))
        return "plain-reply"

    async def discuss_notebook_cell(self, user_message, cell_context):
        self.calls.append(("discuss", user_message, cell_context))
        return "cell-reply"

    async def clear_history(self):
        self.calls.append(("clear_history",))

    async def get_messages(self):
        self.calls.append(("get_messages",))
        return [{"role": "assistant", "content": "hi"}]


def test_build_notebook_cell_prompt_includes_metadata():
    """Cell-aware prompts should embed metadata and fenced source."""
    prompt = build_notebook_cell_prompt(
        "Explain this transformation.",
        {
            "notebook_path": "analysis.ipynb",
            "cell_index": 3,
            "cell_type": "code",
            "language": "python",
            "source": "df = df.dropna()",
        },
    )

    assert "Explain this transformation." in prompt
    assert "`analysis.ipynb`" in prompt
    assert "Cell index: 3" in prompt
    assert "```python" in prompt
    assert "df = df.dropna()" in prompt


def test_build_notebook_cell_prompt_uses_default_message():
    """Empty explicit cell requests should still produce a useful prompt."""
    prompt = build_notebook_cell_prompt("", {"cell_type": "markdown", "source": "# Heading"})

    assert "Please discuss the current notebook cell in detail." in prompt
    assert "# Heading" in prompt


def test_get_or_create_lab_bridge_reuses_existing_agent():
    """The bridge should reuse the notebook agent already injected into the kernel."""
    fake_agent = FakeAgent()
    ipython = SimpleNamespace(user_ns={"agent": fake_agent})

    bridge = get_or_create_lab_bridge(ipython)

    assert isinstance(bridge, SysopLabBridge)
    assert bridge.agent is fake_agent
    assert ipython.user_ns[PUBLIC_BRIDGE_NAME] is bridge


@pytest.mark.asyncio
async def test_handle_lab_request_routes_cell_context():
    """Cell-aware panel requests should be routed through discuss_notebook_cell."""
    fake_agent = FakeAgent()
    ipython = SimpleNamespace(user_ns={"agent": fake_agent})

    result = await handle_lab_request(
        ipython,
        {
            "action": "chat",
            "message": "Why is this cell slow?",
            "cell_context": {"cell_type": "code", "source": "df.apply(func, axis=1)"},
        },
    )

    assert result == {"ok": True, "reply": "cell-reply"}
    assert fake_agent.calls == [
        (
            "discuss",
            "Why is this cell slow?",
            {"cell_type": "code", "source": "df.apply(func, axis=1)"},
        )
    ]


@pytest.mark.asyncio
async def test_handle_lab_request_can_clear_history():
    """The side panel should be able to reset the underlying conversation."""
    fake_agent = FakeAgent()
    ipython = SimpleNamespace(user_ns={"agent": fake_agent})

    result = await handle_lab_request(ipython, {"action": "clear_history"})

    assert result == {"ok": True}
    assert fake_agent.calls == [("clear_history",)]

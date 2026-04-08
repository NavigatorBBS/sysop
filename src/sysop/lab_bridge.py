"""
Kernel bridge used by the JupyterLab side panel.

The frontend sends structured requests through the active notebook kernel and
this module routes them to the shared NotebookChatAgent instance.
"""

import logging
from typing import Any, Dict, Optional

from sysop.chatbot_agent import NotebookCellContext, NotebookChatAgent

logger = logging.getLogger(__name__)

BRIDGE_NAMESPACE_KEY = "__sysop_lab_bridge"
PUBLIC_BRIDGE_NAME = "sysop_lab_bridge"


def _is_agent_like(agent: Any) -> bool:
    """Return True when an object supports the bridge methods we need."""
    required_methods = ("chat", "discuss_notebook_cell", "clear_history", "get_messages")
    return all(callable(getattr(agent, method_name, None)) for method_name in required_methods)


class SysopLabBridge:
    """Bridge that keeps one NotebookChatAgent session per IPython kernel."""

    def __init__(
        self,
        ipython: Any,
        agent: Optional[NotebookChatAgent] = None,
        github_token: Optional[str] = None,
    ):
        self.ipython = ipython
        self.agent = agent or NotebookChatAgent(github_token=github_token)

        self.ipython.user_ns["agent"] = self.agent
        self.ipython.user_ns[PUBLIC_BRIDGE_NAME] = self
        self.ipython.user_ns[BRIDGE_NAMESPACE_KEY] = self

    async def handle_chat(
        self,
        message: str,
        cell_context: Optional[NotebookCellContext] = None,
    ) -> Dict[str, Any]:
        """Send a chat request, optionally enriched with current-cell context."""
        if not message.strip() and not cell_context:
            raise ValueError("Provide a message or include the current cell context.")

        if cell_context:
            response = await self.agent.discuss_notebook_cell(message, cell_context)
        else:
            response = await self.agent.chat(message)

        return {"ok": True, "reply": str(response)}

    async def clear_history(self) -> Dict[str, Any]:
        """Clear the active conversation history."""
        await self.agent.clear_history()
        return {"ok": True}

    async def get_messages(self) -> Dict[str, Any]:
        """Return the current conversation history from the underlying session."""
        messages = await self.agent.get_messages()
        return {"ok": True, "messages": messages}


def get_or_create_lab_bridge(
    ipython: Any,
    github_token: Optional[str] = None,
) -> SysopLabBridge:
    """
    Return the existing kernel bridge or create one on demand.

    Args:
        ipython: The active IPython shell.
        github_token: Optional GitHub Copilot token to pass through.

    Returns:
        A shared bridge for the current kernel.
    """
    if ipython is None:
        raise RuntimeError("An active IPython shell is required for sysop.")

    bridge = ipython.user_ns.get(BRIDGE_NAMESPACE_KEY)
    if isinstance(bridge, SysopLabBridge):
        return bridge

    agent = ipython.user_ns.get("agent")
    if agent is not None and not _is_agent_like(agent):
        raise TypeError("The 'agent' variable exists but does not provide the methods sysop needs.")

    return SysopLabBridge(ipython, agent=agent, github_token=github_token)


async def handle_lab_request(ipython: Any, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a structured request from the JupyterLab side panel.

    Args:
        ipython: The active IPython shell.
        payload: Request payload sent by the frontend.

    Returns:
        A JSON-serializable response dictionary.
    """
    action = str(payload.get("action") or "").strip()
    bridge = get_or_create_lab_bridge(ipython)

    if action == "chat":
        message = str(payload.get("message") or "")
        cell_context = payload.get("cell_context")
        if cell_context is not None and not isinstance(cell_context, dict):
            raise ValueError("cell_context must be an object when provided.")

        return await bridge.handle_chat(message, cell_context=cell_context)

    if action == "clear_history":
        return await bridge.clear_history()

    if action == "get_messages":
        return await bridge.get_messages()

    if action == "ping":
        return {"ok": True, "status": "ready"}

    raise ValueError(f"Unsupported sysop panel action: {action or '<empty>'}")

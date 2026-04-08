"""
sysop: GitHub Copilot SDK-powered Jupyter notebook assistant.

This module provides a chatbot interface for notebook analysis using GitHub's Copilot SDK.
It exposes convenience imports for the Jupyter extension and core agent functionality.
"""

__version__ = "0.1.0"
__author__ = "Christopher Landry"

from sysop.chatbot_agent import (
    MarkdownResponse,
    NotebookCellContext,
    NotebookChatAgent,
    build_notebook_cell_prompt,
)
from sysop.jupyter_extension import (
    handle_lab_request,
    load_ipython_extension,
    unload_ipython_extension,
)
from sysop.lab_bridge import SysopLabBridge, get_or_create_lab_bridge

__all__ = [
    "NotebookChatAgent",
    "NotebookCellContext",
    "MarkdownResponse",
    "SysopLabBridge",
    "build_notebook_cell_prompt",
    "get_or_create_lab_bridge",
    "handle_lab_request",
    "load_ipython_extension",
    "unload_ipython_extension",
]

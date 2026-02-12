"""
sysop: GitHub Copilot SDK-powered Jupyter notebook assistant.

This module provides a chatbot interface for notebook analysis using GitHub's Copilot SDK.
It exposes convenience imports for the Jupyter extension and core agent functionality.
"""

__version__ = "0.1.0"
__author__ = "Christopher Landry"

from sysop.chatbot_agent import MarkdownResponse, NotebookChatAgent
from sysop.jupyter_extension import load_ipython_extension, unload_ipython_extension

__all__ = [
    "NotebookChatAgent",
    "MarkdownResponse",
    "load_ipython_extension",
    "unload_ipython_extension",
]

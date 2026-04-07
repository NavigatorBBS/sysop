"""
Command-line interface for sysop.

Entry point: sysop -c 'your question here'
"""

import argparse
import asyncio
import sys

from dotenv import load_dotenv

load_dotenv()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sysop",
        description="sysop: GitHub Copilot-powered assistant",
    )
    parser.add_argument(
        "-c",
        "--chat",
        metavar="MESSAGE",
        help="Send a message to the assistant and print the response",
    )
    return parser


async def _run_chat(message: str) -> None:
    from sysop.chatbot_agent import NotebookChatAgent

    agent = NotebookChatAgent()
    response = await agent.chat(message, as_markdown=False)
    print(response)


def run() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if not args.chat:
        parser.print_help()
        sys.exit(0)

    asyncio.run(_run_chat(args.chat))

#!/usr/bin/env python
"""
sysop CLI: Command-line interface for testing the sysop chat agent.

Run the GitHub Copilot-powered chat agent from the terminal to test new features
before integrating with Jupyter extension.

Usage:
    python main.py -c "Your question here"
    python main.py --chat "Analyze this code"
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from sysop import NotebookChatAgent

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / ".env")

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sysop",
        description="sysop CLI: Test the sysop chat agent from the terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py -c 'How do I optimize pandas DataFrames?'\n"
            "  python main.py --chat 'Analyze this code for efficiency'\n"
            "\n"
            "Environment:\n"
            "  GITHUB_COPILOT_PAT  Your GitHub Copilot Personal Access Token (required)"
        ),
    )

    parser.add_argument(
        "-c",
        "--chat",
        type=str,
        required=True,
        help="Message to send to the chat agent",
    )

    return parser


async def main(chat_message: str) -> int:
    """
    Main async entry point for the CLI.

    Args:
        chat_message: The message to send to the agent

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        logger.debug(f"Initializing agent with message: {chat_message}")

        # Initialize the chat agent
        agent = NotebookChatAgent()

        # Send message and get response as plain text
        response = await agent.chat(chat_message, as_markdown=False)

        # Print the response
        print(response)

        # Cleanup
        await agent.cleanup()

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(
            "\nPlease set the GITHUB_COPILOT_PAT environment variable with your GitHub token.",
            file=sys.stderr,
        )
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1


def run() -> int:
    """Parse arguments and run the async main function."""
    parser = create_parser()
    args = parser.parse_args()

    # Run the async main function
    return asyncio.run(main(args.chat))


if __name__ == "__main__":
    sys.exit(run())

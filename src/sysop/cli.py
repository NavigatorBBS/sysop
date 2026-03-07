#!/usr/bin/env python
"""
sysop CLI: Command-line interface for testing the sysop chat agent.

Run the GitHub Copilot-powered chat agent from the terminal to test new features
before integrating with Jupyter extension.

Usage:
    sysop -c "Your question here"
    sysop --chat "Analyze this code"
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from sysop import NotebookChatAgent

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# NavigatorBBS Branding
AUTHOR_NAME = "Christopher Landry"
AUTHOR_EMAIL = "sysop@navigatorbbs.net"
PROJECT_VERSION = "0.1.0"


class AnsiColors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # RGB 256-color codes (compatible with most terminals)
    GOLD = "\033[38;5;220m"  # Gold/yellow
    TEAL = "\033[38;5;44m"  # Cyan/teal
    CYAN = "\033[38;5;51m"  # Bright cyan
    YELLOW = "\033[38;5;226m"  # Bright yellow
    GREEN = "\033[38;5;46m"  # Bright green
    WHITE = "\033[38;5;255m"  # White
    GRAY = "\033[38;5;240m"  # Dark gray

    @staticmethod
    def colored(text: str, color: str) -> str:
        """Apply color to text with reset at end."""
        return f"{color}{text}{AnsiColors.RESET}"

    @staticmethod
    def bold(text: str, color: str = "") -> str:
        """Apply bold formatting with optional color."""
        color_code = color or AnsiColors.WHITE
        return f"{AnsiColors.BOLD}{color_code}{text}{AnsiColors.RESET}"


def print_welcome_banner() -> None:
    """Print a stylish welcome banner with NavigatorBBS branding."""
    # Use ASCII-safe alternatives for Windows compatibility
    separator = "=" * 60
    banner = f"""
{AnsiColors.colored(separator, AnsiColors.TEAL)}
{AnsiColors.bold("sysop", AnsiColors.GOLD)} - GitHub Copilot AI Assistant
{AnsiColors.colored(f"v{PROJECT_VERSION}", AnsiColors.CYAN)} | \
{AnsiColors.colored("NavigatorBBS", AnsiColors.GOLD)}
{AnsiColors.colored(separator, AnsiColors.TEAL)}
{AnsiColors.colored("Author:", AnsiColors.WHITE)} \
{AnsiColors.colored(AUTHOR_NAME, AnsiColors.GOLD)}
{AnsiColors.colored("Email: ", AnsiColors.WHITE)} \
{AnsiColors.colored(AUTHOR_EMAIL, AnsiColors.CYAN)}
"""
    print(banner)


class StyledHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom argparse formatter with styled output."""

    def start_section(self, heading):
        """Add colored section headings."""
        if heading:
            heading = AnsiColors.bold(heading, AnsiColors.TEAL)
        super().start_section(heading)

    def _format_usage(self, usage, actions, groups, prefix):
        """Format usage with styling."""
        if prefix is None:
            prefix = "Usage: "
        prefix = AnsiColors.colored(prefix, AnsiColors.GOLD)
        result = super()._format_usage(usage, actions, groups, prefix)
        # Add spacing after usage
        return result + "\n"

    def _format_action(self, action):
        """Style individual arguments."""
        return super()._format_action(action)

    def _format_action_invocation(self, action):
        """Format the invocation (flags) part of an action."""
        result = super()._format_action_invocation(action)
        if not action.option_strings:
            return result
        # Style option strings (like -h, --chat)
        for option in action.option_strings:
            styled = AnsiColors.colored(option, AnsiColors.CYAN)
            result = result.replace(option, styled)
        return result


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sysop",
        description=AnsiColors.bold("sysop CLI", AnsiColors.GOLD)
        + " - Test the sysop chat agent from the terminal",
        formatter_class=StyledHelpFormatter,
        add_help=True,
    )

    parser.add_argument(
        "-c",
        "--chat",
        type=str,
        required=True,
        help="Message to send to the chat agent",
    )

    # Custom epilog with styling
    parser.epilog = (
        f"\n{AnsiColors.bold('Examples:', AnsiColors.YELLOW)}\n"
        f"  sysop -c 'How do I optimize pandas DataFrames?'\n"
        f"  sysop --chat 'Analyze this code for efficiency'\n"
        f"\n"
        f"{AnsiColors.bold('Environment:', AnsiColors.YELLOW)}\n"
        f"  {AnsiColors.colored('GITHUB_COPILOT_PAT', AnsiColors.CYAN)}\n"
        f"    Your GitHub Copilot Personal Access Token (required)\n"
        f"\n"
        f"{AnsiColors.colored('NavigatorBBS', AnsiColors.TEAL)} | "
        f"{AnsiColors.colored(AUTHOR_EMAIL, AnsiColors.GRAY)}\n"
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
    # Print welcome banner before parsing args
    print_welcome_banner()

    parser = create_parser()
    args = parser.parse_args()

    # Run the async main function
    return asyncio.run(main(args.chat))


if __name__ == "__main__":
    sys.exit(run())

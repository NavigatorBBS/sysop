"""
Quick test to verify GitHub Copilot SDK integration.

Run with: python -m pytest test_copilot_integration.py -v
Or: python workspace/src/sysop/test_copilot_integration.py
"""

import asyncio
import os
from types import SimpleNamespace

try:
    import pytest

    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False

    # Mock pytest for standalone execution
    class pytest:
        @staticmethod
        def fail(msg):
            raise AssertionError(msg)

        class mark:
            @staticmethod
            def skipif(condition, reason):
                def decorator(func):
                    return func

                return decorator


class TestCopilotSDKIntegration:
    """Test that the NotebookChatAgent properly uses GitHub Copilot SDK."""

    def test_imports(self):
        """Verify all imports work correctly."""
        try:
            from copilot import CopilotClient, define_tool  # noqa: F401
            from pydantic import BaseModel, Field  # noqa: F401

            from sysop.chatbot_agent import (  # noqa: F401
                MarkdownResponse,
                NotebookChatAgent,
            )

            print("✅ All imports successful")
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")

    def test_agent_initialization(self, monkeypatch):
        """Test agent can be initialized with proper parameters."""
        from sysop import chatbot_agent as chatbot_agent_module

        class FakeSubprocessConfig:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        class FakeClient:
            def __init__(self, config, auto_start=True):
                self.config = config
                self.auto_start = auto_start

        monkeypatch.setattr(chatbot_agent_module, "SubprocessConfig", FakeSubprocessConfig)
        monkeypatch.setattr(chatbot_agent_module, "CopilotClient", FakeClient)
        monkeypatch.setenv("GITHUB_COPILOT_PAT", "test-token-for-initialization")

        agent = chatbot_agent_module.NotebookChatAgent(model="gpt-4o")
        assert agent.model == "gpt-4o"
        assert agent.system_prompt is not None
        assert agent.session is None  # Not initialized yet
        assert isinstance(agent.client.config, FakeSubprocessConfig)
        assert agent.client.config.kwargs["github_token"] == "test-token-for-initialization"
        assert agent.client.config.kwargs["log_level"] == "info"
        assert agent.client.auto_start is True
        print("✅ Agent initialization successful")

    def test_markdown_response(self):
        """Test MarkdownResponse class."""
        from sysop.chatbot_agent import MarkdownResponse

        response = MarkdownResponse("**Hello** World")
        assert str(response) == "**Hello** World"
        assert response._repr_markdown_() == "**Hello** World"
        print("✅ MarkdownResponse works correctly")

    def test_chat_uses_keyword_session_config(self, monkeypatch):
        """Verify chat initializes the session using the current SDK API."""
        from sysop import chatbot_agent as chatbot_agent_module

        class FakeSubprocessConfig:
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        class FakeSession:
            def __init__(self):
                self.handlers = []
                self.sent_prompts = []

            def on(self, handler):
                self.handlers.append(handler)

                def unsubscribe():
                    self.handlers.remove(handler)

                return unsubscribe

            async def send(self, prompt, **kwargs):
                self.sent_prompts.append((prompt, kwargs))
                for handler in list(self.handlers):
                    handler(
                        SimpleNamespace(
                            type=SimpleNamespace(value="assistant.message"),
                            data=SimpleNamespace(content="Mock reply"),
                        )
                    )
                    handler(
                        SimpleNamespace(
                            type=SimpleNamespace(value="session.idle"),
                            data=None,
                        )
                    )
                return "message-1"

        class FakeClient:
            def __init__(self, config, auto_start=True):
                self.config = config
                self.auto_start = auto_start
                self.started = False
                self.create_session_kwargs = None
                self.session = FakeSession()

            async def start(self):
                self.started = True

            async def create_session(self, **kwargs):
                self.create_session_kwargs = kwargs
                return self.session

        monkeypatch.setattr(chatbot_agent_module, "SubprocessConfig", FakeSubprocessConfig)
        monkeypatch.setattr(chatbot_agent_module, "CopilotClient", FakeClient)
        monkeypatch.setenv("GITHUB_COPILOT_PAT", "test-token")

        agent = chatbot_agent_module.NotebookChatAgent(model="gpt-4o")
        response = asyncio.run(agent.chat("Hello from test"))

        assert str(response) == "Mock reply"
        assert agent.client.started is True
        assert agent.client.create_session_kwargs["model"] == "gpt-4o"
        assert agent.client.create_session_kwargs["streaming"] is False
        assert agent.client.create_session_kwargs["system_message"] == {
            "mode": "append",
            "content": agent.system_prompt,
        }
        assert agent.client.create_session_kwargs["on_permission_request"] is not None
        assert agent.client.session.sent_prompts == [("Hello from test", {})]

    @pytest.mark.skipif(
        not os.getenv("GITHUB_COPILOT_PAT"),
        reason="GITHUB_COPILOT_PAT not set - skipping live test",
    )
    def test_live_chat(self):
        """
        Test actual chat with GitHub Copilot SDK.

        Only runs if GITHUB_COPILOT_PAT is set.
        """

        async def run_test():
            from sysop.chatbot_agent import NotebookChatAgent

            agent = NotebookChatAgent(model="gpt-4o")

            try:
                # Simple chat test
                response = await agent.chat("Say 'Hello World' in markdown")
                assert isinstance(response, str)
                assert len(response) > 0
                print(f"✅ Live chat successful: {response[:50]}...")

                # Get messages
                messages = await agent.get_messages()
                assert isinstance(messages, list)
                print(f"✅ Got {len(messages)} messages from session")

            finally:
                await agent.cleanup()
                print("✅ Cleanup successful")

        asyncio.run(run_test())


def run_manual_test():
    """
    Manual test function - run this directly if you have GITHUB_COPILOT_PAT set.

    Usage: python workspace/src/sysop/test_copilot_integration.py
    """
    print("=" * 60)
    print("GitHub Copilot SDK Integration Test")
    print("=" * 60)

    # Check environment
    if not os.getenv("GITHUB_COPILOT_PAT"):
        print("\n❌ GITHUB_COPILOT_PAT not set")
        print("Set it in your environment or .env file to run live tests")
        print("\nRunning basic tests only...\n")
    else:
        print("\n✅ GITHUB_COPILOT_PAT found\n")

    # Run basic tests
    test = TestCopilotSDKIntegration()

    try:
        test.test_imports()
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return

    try:
        test.test_agent_initialization()
    except Exception as e:
        print(f"❌ Initialization test failed: {e}")
        return

    try:
        test.test_markdown_response()
    except Exception as e:
        print(f"❌ MarkdownResponse test failed: {e}")
        return

    print("\n" + "=" * 60)
    print("Basic Tests Complete!")
    print("=" * 60)

    # Run live test if token is available
    if os.getenv("GITHUB_COPILOT_PAT"):
        print("\nRunning live chat test...\n")
        try:
            test.test_live_chat()
            print("\n✅ All tests passed!")
        except Exception as e:
            print(f"\n❌ Live test failed: {e}")
            import traceback

            traceback.print_exc()
    else:
        print("\n💡 To test live chat, set GITHUB_COPILOT_PAT environment variable")


if __name__ == "__main__":
    run_manual_test()

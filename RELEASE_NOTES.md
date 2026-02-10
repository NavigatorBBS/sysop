# MaxBot v0.1.0 Release Notes

**Release Date**: February 2026  
**Tag**: `v0.1.0`

## 🎉 Initial Release

MaxBot is now available as a standalone package! This release represents the extraction of MaxBot from the MaxLab project into its own independent Python package.

## ✨ Features

### Core Functionality

- **GitHub Copilot SDK Integration**: Powered by GitHub's official Copilot SDK for high-quality AI responses
- **NotebookChatAgent**: Main agent class for chat interactions with conversation history management
- **IPython Extension**: Load with `%load_ext maxbot` for seamless Jupyter integration
- **Auto-Rendering Responses**: Markdown responses display automatically without explicit `display()` calls

### Chat Capabilities

- **Multi-turn Conversations**: Maintains context across multiple interactions
- **Code Analysis**: Dedicated `analyze_code()` method for Python code review
- **Plain Text Mode**: Optional plain text responses without markdown formatting
- **Custom System Prompts**: Configurable system prompts for specialized behaviors

### Tool Support

- **Custom Tools**: Register tools using `@define_tool` decorator
- **Flexible Tool Registration**: Add tools before agent initialization
- **Tool Parameter Validation**: Uses Pydantic for type-safe tool parameters

### Developer Experience

- **Async-First API**: Built on asyncio for responsive notebook interactions
- **Type Hints**: Full type annotations for better IDE support
- **Comprehensive Documentation**: README, CONTRIBUTING, and inline docstrings
- **Example Notebooks**: Ready-to-run Jupyter notebook examples

## 📦 Installation

```bash
# From GitHub
pip install git+https://github.com/YOUR_USERNAME/maxbot.git

# From PyPI (coming soon)
pip install maxbot
```

## 🚀 Quick Start

```python
from dotenv import load_dotenv
load_dotenv()

%load_ext maxbot

response = await agent.chat("What are pandas best practices?")
response  # Auto-displays as formatted markdown
```

## 📋 Requirements

- Python 3.10 or higher
- GitHub Copilot SDK
- JupyterLab 4.0+ or IPython 8.0+
- Valid GitHub Copilot PAT

## 🔧 Configuration

Set the `GITHUB_COPILOT_PAT` environment variable:

```env
GITHUB_COPILOT_PAT=your-github-copilot-pat-here
```

Get your token from: https://github.com/settings/tokens

## 📚 Documentation

- **README**: Complete usage guide with examples
- **CONTRIBUTING**: Guidelines for contributors
- **Examples**: Sample code and Jupyter notebooks
- **API Reference**: Inline docstrings for all public methods

## 🐛 Known Issues

- Tools/plugins must be registered before first `chat()` call
- Session initialization is lazy (happens on first use)
- Requires valid GitHub Copilot PAT with appropriate scopes

## 🎯 Breaking Changes

None (initial release)

## 🔄 Migration from MaxLab

If you were using MaxBot from the MaxLab project:

### Before (MaxLab integrated)

```python
%load_ext maxbot
from maxbot.chatbot_agent import NotebookChatAgent
```

### After (Standalone MaxBot)

```python
# Install: pip install maxbot
%load_ext maxbot
from maxbot import NotebookChatAgent
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Originally developed as part of the [MaxLab](https://github.com/NavigatorBBS/maxlab) project
- Built on GitHub's Copilot SDK
- Inspired by the data science community's need for AI-assisted workflows

## 🔗 Links

- **Repository**: https://github.com/YOUR_USERNAME/maxbot
- **Issues**: https://github.com/YOUR_USERNAME/maxbot/issues
- **MaxLab Project**: https://github.com/NavigatorBBS/maxlab

---

Thank you for using MaxBot! We're excited to see what you build with it. 🚀

For questions or feedback, please [open an issue](https://github.com/YOUR_USERNAME/maxbot/issues).

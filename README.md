# 🤖 sysop - GitHub Copilot SDK Jupyter Assistant

[![Lint](https://github.com/NavigatorBBS/sysop/workflows/Lint/badge.svg)](https://github.com/NavigatorBBS/sysop/actions/workflows/lint.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**sysop** is a Jupyter notebook assistant powered by GitHub's Copilot SDK. It provides an AI chatbot interface that integrates seamlessly with JupyterLab, enabling natural language interactions for code analysis, suggestions, and general assistance—all within your notebook environment.

## ✨ Features

- 🤖 **GitHub Copilot Integration** - Powered by GitHub's official Copilot SDK
- 📓 **Jupyter Native** - Load as an IPython extension with `%load_ext sysop`
- 🧭 **JupyterLab Side Panel** - Keep an ongoing `sysop` chat open in the right sidebar
- 🧪 **Current Cell Discussion** - Send the active notebook cell explicitly with a chat request
- 💬 **Auto-Rendering Markdown** - Responses display as formatted markdown automatically
- 🔄 **Conversation History** - Maintains context across multiple interactions
- 🛠️ **Extensible Tools** - Register custom tools using `@define_tool` decorator
- ⚡ **Async-First** - Built on asyncio for responsive notebook experience

## 📦 Installation

### From PyPI (when published)

```bash
pip install sysop
```

### From Source

```bash
git clone https://github.com/NavigatorBBS/sysop.git
cd sysop
pip install -e ".[dev]"
npm install
npm run build
```

If you are developing from an editable checkout and want JupyterLab to load the side panel extension
from your working tree, also run:

```bash
jupyter labextension develop . --overwrite
```

Wheel installs include the prebuilt labextension assets automatically, so the extra
`jupyter labextension develop` step is only needed for local editable development.

## 🚀 Quick Start

### 1. Set up your GitHub Copilot token

Create a `.env` file or set an environment variable:

```env
GITHUB_COPILOT_PAT=your-github-copilot-pat-here
```

Get your token from: https://github.com/settings/tokens (requires copilot scope)

### 2. Open the JupyterLab side panel

Start JupyterLab:

```bash
jupyter lab
```

The `sysop` panel opens in the right sidebar when the extension loads. You can also reopen it from
the Command Palette with **Open sysop Chat**.

Use the panel to:

- Keep a persistent chat open for the active notebook kernel
- Send ordinary freeform questions with **Send**
- Use **Discuss current cell** to attach the active cell only for that request
- Reset the conversation with **Clear chat**

### 3. Use the CLI

You can test the agent from your terminal:

```bash
sysop -c "How can I optimize this pandas DataFrame?"
sysop --chat "Analyze this code for efficiency"
```

### 4. Load the extension in a Jupyter notebook

```python
from dotenv import load_dotenv
load_dotenv()

%load_ext sysop
```

This automatically:
- Initializes the `NotebookChatAgent` with your GitHub Copilot credentials
- Injects the `agent` variable into your notebook namespace
- Makes `display()` and `Markdown()` utilities available

### 5. Chat with the agent

```python
# Simple usage - response auto-displays as markdown
response = await agent.chat("How can I optimize this pandas DataFrame?")
response
```

## 📚 Usage Examples

### CLI Usage

```bash
# Ask questions
sysop -c "What's the best way to handle missing data in pandas?"

# For longer questions with special characters, use quotes
sysop --chat "How do I optimize DataFrame groupby operations?"
```

### Jupyter Extension Usage

```python
# Ask questions
response = await agent.chat("What's the best way to handle missing data in pandas?")
response  # Auto-displays as formatted markdown

# For plain text without markdown formatting
plain_text = await agent.chat("Your question", as_markdown=False)
```

### JupyterLab Side Panel Usage

The JupyterLab panel keeps a persistent chat session tied to the active notebook kernel.

- **Send** submits a normal chat message.
- **Discuss current cell** sends the active cell source and metadata with that one request.
- **Clear chat** resets the underlying `NotebookChatAgent` session.

If you want to work directly in notebook cells as well, `%load_ext sysop` still injects
`agent`, `display`, and `Markdown` into the IPython namespace.

### Code Analysis

```python
# Analyze code snippets
code = '''
df = pd.read_csv('data.csv')
df = df[df['value'] > 0]
result = df.groupby('category').sum()
'''

response = await agent.analyze_code(code, context="data aggregation pipeline")
response
```

### Conversation Management

```python
# Get conversation history
messages = await agent.get_messages()
print(f"Conversation has {len(messages)} messages")

# Clear history to start fresh
await agent.clear_history()

# Cleanup when done (releases resources)
await agent.cleanup()
```

### Custom Tools (Advanced)

Create custom tools that the agent can use:

```python
from pydantic import BaseModel, Field
from copilot import define_tool

class AnalyzeCodeParams(BaseModel):
    code: str = Field(description="Python code to analyze")
    context: str = Field(default="", description="Optional context")

@define_tool(description="Analyze Python code for quality and best practices")
async def analyze_code_tool(params: AnalyzeCodeParams) -> str:
    # Your analysis logic here
    return f"Analyzing {len(params.code)} characters of code..."

# Register tools before first use
agent = NotebookChatAgent(model="gpt-4o")
agent.tools = [analyze_code_tool]

response = await agent.chat("Can you analyze my code?")
```

## 🔧 Configuration

sysop uses environment variables for configuration:

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_COPILOT_PAT` | Yes | Your GitHub Copilot Personal Access Token |

### Programmatic Initialization

You can also initialize the agent programmatically:

```python
from sysop import NotebookChatAgent

agent = NotebookChatAgent(
    github_token="your-token",
    model="gpt-4o",
    system_prompt="Custom system prompt..."
)
```

## 📖 API Reference

### `NotebookChatAgent`

The main chatbot agent class.

**Methods:**

- `async chat(user_message: str, as_markdown: bool = True)` - Send a message and get a response
- `async analyze_code(code: str, context: Optional[str] = None)` - Analyze Python code
- `async suggest_notebook_improvements(notebook_summary: str)` - Get notebook improvement suggestions
- `async get_messages()` - Get conversation history
- `async clear_history()` - Clear conversation and start fresh
- `async cleanup()` - Clean up resources (call when done)
- `add_plugin(plugin_instance, plugin_name)` - Register a plugin (before first chat)

### `MarkdownResponse`

A string subclass that auto-renders as Markdown in Jupyter notebooks.

### IPython Extension

- `load_ipython_extension(ipython)` - Called by `%load_ext sysop`
- `unload_ipython_extension(ipython)` - Called by `%unload_ext sysop`

## 🧪 Development

### Setup Development Environment

```bash
git clone https://github.com/NavigatorBBS/sysop.git
cd sysop
pip install -e ".[dev]"
npm install
npm run build
```

To load the side panel from an editable checkout while developing JupyterLab UI changes:

```bash
jupyter labextension develop . --overwrite
```

### Run Tests

```bash
pytest tests/ -v
```

### Linting

```bash
# Format code
black src/ tests/ examples/
isort src/ tests/ examples/

# Check style
flake8 src/ tests/ examples/ --max-line-length=100
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- Inspired by the need for AI-assisted data science workflows

## 🔗 Links

- **Documentation**: https://github.com/NavigatorBBS/sysop/wiki
- **Issues**: https://github.com/NavigatorBBS/sysop/issues
- **PyPI**: https://pypi.org/project/sysop/ (coming soon)

## ⚠️ Requirements

- Python 3.10 or higher
- GitHub Copilot subscription and access token
- JupyterLab 4.0+ or IPython 8.0+

## 🐛 Known Issues

- Tools/plugins must be registered before the first `chat()` call
- Session creation is lazy (initialized on first use)
- Requires valid GitHub Copilot PAT with appropriate scopes

## 📝 Changelog

### v0.1.0 (Initial Release)

- Core `NotebookChatAgent` with GitHub Copilot SDK integration
- IPython extension for seamless Jupyter integration
- Auto-rendering markdown responses
- Conversation history management
- Custom tool support via `@define_tool`
- Async-first API design

---

Made with ❤️ by [Christopher Landry](https://github.com/NavigatorBBS)

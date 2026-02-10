# Contributing to MaxBot

Thank you for your interest in contributing to MaxBot! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear description** of the issue
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Environment details** (Python version, OS, JupyterLab version)
- **Code samples** or error messages if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear description** of the proposed feature
- **Use case** explaining why this would be useful
- **Possible implementation** if you have ideas

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Write clear, descriptive commit messages
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
3. **Test your changes**:
   ```bash
   pytest tests/ -v
   black src/ tests/ examples/
   isort src/ tests/ examples/
   flake8 src/ tests/ examples/ --max-line-length=100
   ```
4. **Submit your pull request**:
   - Reference any related issues
   - Describe what your changes do
   - Include screenshots for UI changes

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- GitHub Copilot SDK access

### Setup Steps

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/maxbot.git
   cd maxbot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GITHUB_COPILOT_PAT
   ```

## Code Style

### Python Style Guide

- Follow **PEP 8** conventions
- Use **type hints** for function arguments and return values
- Maximum line length: **100 characters**
- Use **docstrings** (Google style) for all public functions/classes
- Run **black** and **isort** before committing

### Example:

```python
from typing import Optional

async def my_function(param: str, optional: Optional[int] = None) -> str:
    """
    Brief description of what the function does.
    
    Args:
        param: Description of param
        optional: Description of optional parameter
        
    Returns:
        Description of return value
    """
    return result
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_copilot_integration.py -v

# Run with coverage
pytest --cov=maxbot tests/
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use `pytest` conventions and fixtures
- Test both success and failure cases
- Mock external dependencies (GitHub Copilot SDK calls)

## Documentation

- Update **README.md** for user-facing changes
- Add **docstrings** to all public APIs
- Include **examples** for new features
- Update **CHANGELOG** for notable changes

## Commit Messages

Use clear, descriptive commit messages:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

Examples:
- `feat: add custom tool registration support`
- `fix: resolve session cleanup race condition`
- `docs: update README with new examples`

## Questions?

Feel free to open an issue with the `question` label if you need help or clarification.

Thank you for contributing to MaxBot! 🚀

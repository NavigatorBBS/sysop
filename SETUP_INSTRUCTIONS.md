# sysop Repository Setup Instructions

This document provides step-by-step instructions for setting up the sysop GitHub repository.

## Prerequisites

- GitHub account with Copilot access
- Git installed locally
- Python 3.10+ installed

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `sysop`
   - **Description**: "GitHub Copilot SDK-powered Jupyter notebook assistant"
   - **Visibility**: Public (or Private if preferred)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

## Step 2: Initialize Local Git Repository

Navigate to the sysop directory and initialize git:

```powershell
cd C:\Users\chris\code\sysop

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "feat: initial release of sysop v0.1.0

- Core NotebookChatAgent with GitHub Copilot SDK integration
- IPython extension for seamless Jupyter integration
- Auto-rendering markdown responses
- Conversation history management
- Custom tool support via @define_tool
- Comprehensive documentation and examples"
```

## Step 3: Connect to GitHub

```powershell
# Add remote origin
git remote add origin https://github.com/NavigatorBBS/sysop.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Configure Repository Settings

### Enable GitHub Actions

1. Go to your repository on GitHub
2. Click on **Actions** tab
3. Enable workflows (if prompted)
4. The lint workflow should appear under "All workflows"

### Add Repository Topics

1. Go to repository home page
2. Click the gear icon next to "About"
3. Add topics: `jupyter`, `copilot`, `ai`, `chatbot`, `notebook`, `python`, `jupyter-notebook`, `jupyter-extension`

### Set Up Branch Protection (Optional)

1. Go to **Settings** > **Branches**
2. Add branch protection rule for `main`:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Enable "Lint" workflow as required check

## Step 5: Update URLs in Files

If needed, verify that all URLs reference NavigatorBBS/sysop:

- `README.md` (multiple locations)
- `pyproject.toml` (URLs section)

Then commit and push:

```powershell
git add README.md pyproject.toml
git commit -m "docs: update repository URLs"
git push
```

## Step 6: Create v0.1.0 Release

1. Go to repository **Releases** page
2. Click **Draft a new release**
3. Fill in release details:
   - **Tag version**: `v0.1.0`
   - **Release title**: `sysop v0.1.0 - Initial Release`
   - **Description**: Copy content from `RELEASE_NOTES.md`
4. Click **Publish release**

## Step 7: Test Installation

Test that the package can be installed from GitHub:

```powershell
# In a new virtual environment
python -m venv test-env
.\test-env\Scripts\activate

# Install from GitHub
pip install git+https://github.com/NavigatorBBS/sysop.git

# Test import
python -c "from sysop import NotebookChatAgent; print('Success!')"
```

## Optional: Publish to PyPI

To make the package installable via `pip install sysop`:

### 1. Create PyPI Account

- Register at https://pypi.org/account/register/
- Set up 2FA
- Create API token at https://pypi.org/manage/account/token/

### 2. Build and Upload

```powershell
# Install build tools
pip install build twine

# Build distribution
python -m build

# Upload to PyPI (will prompt for credentials)
python -m twine upload dist/*
```

### 3. Verify

```powershell
pip install sysop
```

## Repository Structure

After setup, your repository should look like:

```
sysop/
├── .github/
│   └── workflows/
│       └── lint.yml
├── examples/
│   ├── basic_usage.ipynb
│   └── example_usage.py
├── src/
│   └── sysop/
│       ├── __init__.py
│       ├── chatbot_agent.py
│       └── jupyter_extension.py
├── tests/
│   └── test_copilot_integration.py
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── RELEASE_NOTES.md
├── SETUP_INSTRUCTIONS.md (this file)
└── pyproject.toml
```

## Troubleshooting

### Push rejected

If you get "repository not found" or authentication errors:
- Verify repository URL: `git remote -v`
- Check GitHub username and permissions
- Use SSH instead of HTTPS: `git remote set-url origin git@github.com:NavigatorBBS/sysop.git`

### GitHub Actions not running

- Check that workflows are enabled in repository settings
- Verify `.github/workflows/lint.yml` exists
- Check Actions tab for error messages

## Next Steps

1. Create announcement or blog post about the new package
2. Share on relevant communities (Reddit, Twitter, etc.)
3. Consider creating a documentation site (GitHub Pages, Read the Docs)

---

**Congratulations!** Your sysop repository is now set up and ready for contributions! 🎉

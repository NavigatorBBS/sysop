# sysop CLI Setup Script
# Creates a conda environment and installs the sysop package

param(
    [string]$EnvName = "sysop",
    [string]$PythonVersion = "3.11"
)

Write-Host "Setting up sysop environment..." -ForegroundColor Cyan

# Create conda environment
Write-Host "Creating conda environment '$EnvName' with Python $PythonVersion..." -ForegroundColor Yellow
conda create -n $EnvName python=$PythonVersion -y

# Activate the environment
Write-Host "Activating conda environment..." -ForegroundColor Yellow
conda activate $EnvName

# Install the package in editable mode
Write-Host "Installing sysop package..." -ForegroundColor Yellow
pip install -e .

# Verify installation
Write-Host "Verifying installation..." -ForegroundColor Yellow
python main.py --help

Write-Host "`nSetup complete! ✓" -ForegroundColor Green
Write-Host "To activate the environment, run: conda activate $EnvName" -ForegroundColor Cyan
Write-Host "To use the CLI, run: python main.py -c 'Your question here'" -ForegroundColor Cyan
Write-Host "`nDon't forget to set GITHUB_COPILOT_PAT environment variable!" -ForegroundColor Magenta

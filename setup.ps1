# sysop CLI Setup Script
# Creates a conda environment and installs the sysop package

param(
    [string]$EnvName = "sysop",
    [string]$PythonVersion = "3.11"
)

function Show-BigLogo {
    $reset = "`e[0m"

    $gold   = "`e[38;2;230;200;120m"
    $yellow = "`e[38;2;220;230;180m"
    $teal   = "`e[38;2;80;200;200m"

    Write-Host "$gold███╗   ██╗ █████╗ ██╗   ██╗██╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗$reset"
    Write-Host "$yellow████╗  ██║██╔══██╗██║   ██║██║██╔════╝ ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗$reset"
    Write-Host "$yellow██╔██╗ ██║███████║██║   ██║██║██║  ███╗███████║   ██║   ██║   ██║██████╔╝$reset"
    Write-Host "$teal██║╚██╗██║██╔══██║╚██╗ ██╔╝██║██║   ██║██╔══██║   ██║   ██║   ██║██╔══██╗$reset"
    Write-Host "$teal██║ ╚████║██║  ██║ ╚████╔╝ ██║╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║$reset"
    Write-Host "$teal╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝$reset"

    $reset = "`e[0m"
    $teal  = "`e[38;2;80;200;200m"

    Write-Host ""
    Write-Host "$teal        ══▶   ██████╗ ██████╗ ███████╗   ◀══$reset"
    Write-Host "$teal              ██╔══██╗██╔══██╗██╔════╝$reset"
    Write-Host "$teal              ██████╔╝██████╔╝███████╗$reset"
    Write-Host "$teal              ██╔══██╗██╔══██╗╚════██║$reset"
    Write-Host "$teal              ██████╔╝██████╔╝███████║$reset"
    Write-Host ""
    Start-Sleep -Milliseconds 150
    Write-Host "`e[2mNavigator BBS Environment Ready`e[0m"
}

function Show-BbsHeader {
    param (
        [string]$Title = "NavigatorBBS MaxLab Setup"
    )

    $padding = 4
    $width   = $Title.Length + ($padding * 2)

    $border  = "+" + ("-" * $width) + "+"
    $spaces  = " " * $padding
    $line    = "|$spaces$Title$spaces|"

    Write-Output ""
    Write-Output $border
    Write-Output $line
    Write-Output $border
    Write-Output ""
}

Show-BigLogo
Show-BbsHeader -Title "Setting up sysop environment..." -ForegroundColor Cyan

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

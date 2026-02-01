param(
    [string]$InputFile = "LAUNCHER.ps1",
    [string]$OutputFile = "LAUNCHER.exe",
    [string]$IconFile = $null,
    [switch]$RequireAdmin = $true,
    [switch]$Install = $false
)

Write-Host "Fusion 360 Copilot Assistant - EXE Converter" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if ps2exe is installed
$ps2exe = Get-Module -Name ps2exe -ListAvailable

if (-not $ps2exe) {
    Write-Host "ps2exe module not found. Installing..." -ForegroundColor Yellow
    
    try {
        Install-Module -Name ps2exe -Scope CurrentUser -Force -ErrorAction Stop
        Write-Host "ps2exe installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Failed to install ps2exe: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "To install manually, run:" -ForegroundColor Yellow
        Write-Host "  Install-Module -Name ps2exe -Scope CurrentUser -Force" -ForegroundColor Gray
        exit 1
    }
}

# Import the module
Import-Module ps2exe

Write-Host "Converting $InputFile to $OutputFile..." -ForegroundColor Cyan

# Build conversion parameters
$params = @{
    inputFile = $InputFile
    outputFile = $OutputFile
}

if ($IconFile -and (Test-Path $IconFile)) {
    $params['iconFile'] = $IconFile
    Write-Host "Using icon: $IconFile" -ForegroundColor Gray
}

if ($RequireAdmin) {
    $params['requireAdmin'] = $true
    Write-Host "Requiring administrator privileges" -ForegroundColor Gray
}

# Convert
try {
    Invoke-ps2exe @params -ErrorAction Stop
    Write-Host "✓ Conversion successful!" -ForegroundColor Green
    Write-Host "Output: $(Get-Item $OutputFile)" -ForegroundColor Green
} catch {
    Write-Host "✗ Conversion failed: $_" -ForegroundColor Red
    exit 1
}

# Optional: Install to PATH
if ($Install) {
    Write-Host ""
    Write-Host "Installing to PATH..." -ForegroundColor Cyan
    
    $programFiles = $env:ProgramFiles
    $appPath = Join-Path $programFiles "Assist360"
    
    if (-not (Test-Path $appPath)) {
        New-Item -ItemType Directory -Path $appPath -Force | Out-Null
    }
    
    Copy-Item -Path $OutputFile -Destination $appPath -Force
    Write-Host "✓ Installed to: $appPath" -ForegroundColor Green
    
    # Add to PATH if not already there
    $pathValue = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($pathValue -notmatch [regex]::Escape($appPath)) {
        [Environment]::SetEnvironmentVariable("Path", "$pathValue;$appPath", "User")
        Write-Host "✓ Added to PATH" -ForegroundColor Green
        Write-Host "Note: You may need to restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "You can now:" -ForegroundColor Cyan
Write-Host "  1. Double-click $OutputFile to launch" -ForegroundColor Gray
Write-Host "  2. Create a shortcut for the Start Menu" -ForegroundColor Gray
Write-Host "  3. Run from command line: $OutputFile" -ForegroundColor Gray

param(
    [switch]$Test = $false,
    [switch]$Validate = $false
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Configuration
$AppName = "Fusion 360 Copilot Assistant"
$AppVersion = "0.1.0"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$AddinPath = Join-Path $ScriptDir "fusion_copilot_addin"
$FusionAddinPath = "$env:APPDATA\Autodesk\Fusion 360\API\addins"

# Log file
$LogFile = Join-Path $ScriptDir "copilot_launcher.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Add-Content -Path $LogFile -Value $logMessage
    Write-Host $logMessage
}

function Show-Error {
    param([string]$Title, [string]$Message)
    Write-Log "ERROR: $Title - $Message"
    [System.Windows.Forms.MessageBox]::Show($Message, $Title, [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
}

function Show-Info {
    param([string]$Title, [string]$Message)
    Write-Log "INFO: $Title - $Message"
    [System.Windows.Forms.MessageBox]::Show($Message, $Title, [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
}

function Show-Warning {
    param([string]$Title, [string]$Message)
    Write-Log "WARNING: $Title - $Message"
    [System.Windows.Forms.MessageBox]::Show($Message, $Title, [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Warning)
}

Write-Log "=========================================="
Write-Log "$AppName Launcher v$AppVersion"
Write-Log "=========================================="
Write-Log "Working directory: $ScriptDir"
Write-Log "Addin path: $AddinPath"

# Test mode - run validation only
if ($Test -or $Validate) {
    Write-Log "Running in validation mode"
    & "$ScriptDir\RUN.ps1"
    exit $LASTEXITCODE
}

# Step 1: Validate project structure
Write-Log "Step 1: Validating project structure..."
if (-not (Test-Path $AddinPath)) {
    Show-Error "Missing Add-in", "Fusion 360 Copilot add-in not found at:`n$AddinPath"
    exit 1
}

if (-not (Test-Path "$AddinPath/manifest.json")) {
    Show-Error "Invalid Add-in", "Add-in manifest not found"
    exit 1
}

Write-Log "Add-in structure validated"

# Step 2: Check if Fusion 360 is installed
Write-Log "Step 2: Checking for Fusion 360 installation..."
$fusionPath = $null
$possiblePaths = @(
    "C:\Program Files\Autodesk\Fusion 360\Fusion360.exe",
    "$env:ProgramFiles\Autodesk\Fusion 360\Fusion360.exe",
    "$env:ProgramFiles(x86)\Autodesk\Fusion 360\Fusion360.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $fusionPath = $path
        break
    }
}

if (-not $fusionPath) {
    Show-Error "Fusion 360 Not Found", "Fusion 360 is not installed on this system.`n`nPlease install Fusion 360 from https://www.autodesk.com/products/fusion-360"
    exit 1
}

Write-Log "Found Fusion 360 at: $fusionPath"

# Step 3: Check/install add-in
Write-Log "Step 3: Setting up add-in..."
if (-not (Test-Path $FusionAddinPath)) {
    Write-Log "Creating Fusion 360 add-ins directory..."
    New-Item -ItemType Directory -Path $FusionAddinPath -Force | Out-Null
}

# Create symbolic link or copy
$addinInstallPath = Join-Path $FusionAddinPath "Assist360"
if (-not (Test-Path $addinInstallPath)) {
    Write-Log "Copying add-in to Fusion add-ins folder..."
    try {
        Copy-Item -Path $AddinPath -Destination $addinInstallPath -Recurse -Force
        Write-Log "Add-in copied successfully"
    } catch {
        Show-Error "Installation Failed", "Failed to copy add-in to Fusion folder:`n$_"
        exit 1
    }
} else {
    Write-Log "Add-in already installed at $addinInstallPath"
}

# Step 4: Launch Fusion 360
Write-Log "Step 4: Launching Fusion 360..."
Write-Log "Executing: $fusionPath"

try {
    $process = Start-Process -FilePath $fusionPath -PassThru
    Write-Log "Fusion 360 started with PID: $($process.Id)"
    
    Show-Info "Fusion 360 Launched", "Fusion 360 is starting...`n`nThe Copilot Assistant panel will appear in the right sidebar once Fusion 360 loads.`n`nTo access it: View > Copilot Assistant"
    
    # Wait for process to exit
    Wait-Process -InputObject $process
    Write-Log "Fusion 360 closed"
} catch {
    Show-Error "Launch Failed", "Failed to launch Fusion 360:`n$_"
    exit 1
}

Write-Log "Application shutdown"
Write-Log "=========================================="

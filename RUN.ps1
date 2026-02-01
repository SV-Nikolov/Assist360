param([switch]$Verbose = $false)

$ErrorActionPreference = "Stop"
$FailedTests = 0
$PassedTests = 0

function Write-Success {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
    $Script:PassedTests++
}

function Write-Error {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    $Script:FailedTests++
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Blue
    Write-Host " $Message" -ForegroundColor Blue
    Write-Host ("=" * 60) -ForegroundColor Blue
    Write-Host ""
}

# Test 1: Project Structure
Write-Header "1. PROJECT STRUCTURE"

$requiredDirs = @(
    "fusion_copilot_addin",
    "fusion_copilot_addin/core",
    "fusion_copilot_addin/ui",
    "fusion_copilot_addin/tools",
    "fusion_copilot_addin/scripts"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Success "Directory exists: $dir"
    } else {
        Write-Error "Directory missing: $dir"
    }
}

$requiredFiles = @(
    "fusion_copilot_addin/manifest.json",
    "fusion_copilot_addin/main.py",
    "fusion_copilot_addin/config.py",
    "fusion_copilot_addin/core/orchestrator.py",
    "fusion_copilot_addin/core/context.py",
    "fusion_copilot_addin/core/executor.py",
    "fusion_copilot_addin/core/codegen.py",
    "fusion_copilot_addin/ui/panel.html",
    "fusion_copilot_addin/ui/panel.css",
    "fusion_copilot_addin/ui/panel.js",
    "fusion_copilot_addin/tools/filesystem.py",
    "fusion_copilot_addin/README.md"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Success "File exists: $file"
    } else {
        Write-Error "File missing: $file"
    }
}

# Test 2: Python Syntax Validation
Write-Header "2. PYTHON SYNTAX VALIDATION"

$pythonFiles = Get-ChildItem -Path "fusion_copilot_addin" -Filter "*.py" -Recurse

if ($pythonFiles.Count -eq 0) {
    Write-Error "No Python files found"
} else {
    Write-Info "Found $($pythonFiles.Count) Python files"
    
    $pythonAvailable = $null -ne (Get-Command python -ErrorAction SilentlyContinue)
    
    if ($pythonAvailable) {
        foreach ($file in $pythonFiles) {
            try {
                $output = python -m py_compile $file.FullName 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Python syntax valid: $($file.Name)"
                } else {
                    Write-Error "Python syntax error in $($file.Name)"
                }
            } catch {
                Write-Error "Failed to check syntax of $($file.Name)"
            }
        }
    } else {
        Write-Info "Python not found - skipping syntax check (install Python 3.8+ to enable)"
        foreach ($file in $pythonFiles) {
            Write-Info "Skipped: $($file.Name)"
        }
    }
}

# Test 3: Configuration Validation
Write-Header "3. CONFIGURATION VALIDATION"

$manifestPath = "fusion_copilot_addin/manifest.json"
try {
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    if ($manifest.id -eq "fusion_copilot_assistant") {
        Write-Success "manifest.json is valid with correct ID"
    } else {
        Write-Error "manifest.json has incorrect ID: $($manifest.id)"
    }
} catch {
    Write-Error "manifest.json is invalid JSON"
}

# Test 4: HTML/CSS/JS Validation
Write-Header "4. WEB ASSETS VALIDATION"

$htmlPath = "fusion_copilot_addin/ui/panel.html"
if (Test-Path $htmlPath) {
    $htmlContent = Get-Content $htmlPath -Raw
    if ($htmlContent -match "<html" -and $htmlContent -match "</html>") {
        Write-Success "panel.html has valid structure"
    } else {
        Write-Error "panel.html missing HTML structure"
    }
}

$cssPath = "fusion_copilot_addin/ui/panel.css"
if (Test-Path $cssPath) {
    $cssContent = Get-Content $cssPath -Raw
    if ($cssContent -match ":root" -and $cssContent -match "\.header") {
        Write-Success "panel.css has valid content"
    } else {
        Write-Error "panel.css missing expected CSS"
    }
}

$jsPath = "fusion_copilot_addin/ui/panel.js"
if (Test-Path $jsPath) {
    $jsContent = Get-Content $jsPath -Raw
    if ($jsContent -match "function" -and $jsContent -match "addEventListener") {
        Write-Success "panel.js has valid content"
    } else {
        Write-Error "panel.js missing JavaScript"
    }
}

# Test 5: Documentation
Write-Header "5. DOCUMENTATION"

$docFiles = @(
    "fusion_copilot_addin/README.md",
    "fusion_copilot_addin/ARCHITECTURE.md",
    "fusion_copilot_addin/REQUIREMENTS.md"
)

foreach ($file in $docFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content.Length -gt 100) {
            Write-Success "Documentation: $file"
        } else {
            Write-Error "Documentation too small: $file"
        }
    } else {
        Write-Error "Documentation missing: $file"
    }
}

# Test 6: Core Module Structure
Write-Header "6. CORE MODULES"

$coreModules = @(
    @{name = "orchestrator.py"; required = @("Orchestrator", "process_chat_message") },
    @{name = "context.py"; required = @("ContextCapture", "get_runtime_context") },
    @{name = "executor.py"; required = @("CodeExecutor", "run_code") },
    @{name = "codegen.py"; required = @("CodeGenerator", "build_prompt") }
)

foreach ($module in $coreModules) {
    $path = "fusion_copilot_addin/core/$($module.name)"
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        $found = $true
        foreach ($item in $module.required) {
            if ($content -notmatch $item) {
                $found = $false
                Write-Error "$($module.name) missing: $item"
                break
            }
        }
        if ($found) {
            Write-Success "$($module.name) has all required components"
        }
    } else {
        Write-Error "Module missing: $($module.name)"
    }
}

# Summary
Write-Header "TEST SUMMARY"

$total = $PassedTests + $FailedTests
Write-Host ""
Write-Host "Passed: $PassedTests" -ForegroundColor Green
Write-Host "Failed: $FailedTests" -ForegroundColor $(if ($FailedTests -eq 0) { "Green" } else { "Red" })
Write-Host "Total:  $total" -ForegroundColor Cyan
Write-Host ""

if ($FailedTests -eq 0) {
    Write-Host "OK - ALL TESTS PASSED - READY TO COMMIT" -ForegroundColor Green -BackgroundColor DarkGreen
    exit 0
} else {
    Write-Host "FAIL - SOME TESTS FAILED - PLEASE FIX" -ForegroundColor Red -BackgroundColor DarkRed
    exit 1
}

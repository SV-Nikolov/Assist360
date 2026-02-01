# Fusion 360 Copilot Assistant - Launcher Guide

## Quick Start

### Option 1: Double-Click Batch File (Easiest)
Simply double-click `LAUNCHER.bat` to launch Fusion 360 with Copilot Assistant.

### Option 2: PowerShell
```powershell
.\LAUNCHER.ps1
```

### Option 3: Convert to EXE (Advanced)

If you want a standalone `.exe` file without batch/PowerShell:

#### Using PS2EXE (Recommended)

1. **Install PS2EXE**:
   ```powershell
   Install-Module -Name ps2exe -Scope CurrentUser -Force
   ```

2. **Convert to EXE**:
   ```powershell
   Invoke-ps2exe -inputFile "LAUNCHER.ps1" -outputFile "LAUNCHER.exe" -iconFile "icon.ico" -requireAdmin
   ```

3. **Result**: `LAUNCHER.exe` - A standalone executable

#### Alternative: Using Advanced Installer

For commercial deployment, use Advanced Installer to create a professional Windows installer.

## What the Launcher Does

### Startup Sequence

1. ✓ **Validates** add-in structure and manifest
2. ✓ **Checks** for Fusion 360 installation
3. ✓ **Installs** add-in to Fusion add-ins folder (if needed)
4. ✓ **Launches** Fusion 360
5. ✓ **Logs** all activity to `copilot_launcher.log`

### Add-in Installation

The launcher automatically:
- Copies the add-in to: `%APPDATA%\Autodesk\Fusion 360\API\addins\Assist360\`
- Creates necessary directories
- Handles errors gracefully

### Log File

All activity is logged to: `copilot_launcher.log`

Example log output:
```
[2026-02-01 10:30:45] ==========================================
[2026-02-01 10:30:45] Fusion 360 Copilot Assistant Launcher v0.1.0
[2026-02-01 10:30:45] ==========================================
[2026-02-01 10:30:45] Working directory: C:\Source\Assist360
[2026-02-01 10:30:45] Step 1: Validating project structure...
[2026-02-01 10:30:45] Add-in structure validated
[2026-02-01 10:30:45] Step 2: Checking for Fusion 360 installation...
[2026-02-01 10:30:46] Found Fusion 360 at: C:\Program Files\Autodesk\Fusion 360\Fusion360.exe
[2026-02-01 10:30:46] Step 3: Setting up add-in...
[2026-02-01 10:30:46] Add-in copied successfully
[2026-02-01 10:30:46] Step 4: Launching Fusion 360...
[2026-02-01 10:30:47] Fusion 360 started with PID: 12345
```

## Command-Line Options

### Validation Mode
```powershell
.\LAUNCHER.ps1 -Validate
.\LAUNCHER.ps1 -Test
```

Validates the add-in without launching Fusion 360.

## Troubleshooting

### "Fusion 360 Not Found"
- Install Fusion 360 from https://www.autodesk.com/products/fusion-360
- Ensure you install to default location (C:\Program Files\Autodesk\Fusion 360\)

### "Add-in not appearing in Fusion"
- Check the log file: `copilot_launcher.log`
- Restart Fusion 360
- Go to View > Copilot Assistant to show the panel

### "Access Denied" when installing
- Run launcher as Administrator
- Or manually copy the add-in folder to: `%APPDATA%\Autodesk\Fusion 360\API\addins\Assist360\`

### Port Already in Use
- If using local LLM, ensure Ollama is running on port 11434
- Check: `http://localhost:11434/api/tags`

## Files

- **LAUNCHER.bat** - Windows batch launcher (easiest for users)
- **LAUNCHER.ps1** - PowerShell launcher (with detailed logging)
- **copilot_launcher.log** - Activity log

## Creating a Desktop Shortcut

1. Right-click on `LAUNCHER.bat`
2. Select "Send to > Desktop (create shortcut)"
3. Right-click shortcut → Properties
4. Change icon if desired
5. Double-click to launch

## Creating a Start Menu Entry

Windows 11/10:
1. Create shortcut to `LAUNCHER.bat`
2. Place in: `C:\Users\[User]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\`
3. Rename to "Fusion 360 Copilot Assistant"

## Next Steps

Once Fusion 360 launches:
1. Wait for it to fully load (30-60 seconds)
2. Look for "Copilot Assistant" panel on the right
3. If not visible: View > Copilot Assistant
4. Start typing your design requests!

## Support

For issues:
1. Check `copilot_launcher.log` for detailed error messages
2. Run with `-Test` flag to validate everything
3. Open an issue on GitHub: https://github.com/SV-Nikolov/Assist360/issues

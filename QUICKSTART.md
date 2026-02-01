# Getting Started - Quick Launch Guide

## 🚀 Quick Start (30 seconds)

### Option 1: Simple Double-Click (Recommended)
1. Double-click **`LAUNCHER.bat`**
2. Wait for Fusion 360 to launch (60 seconds)
3. Look for **"Copilot Assistant"** panel on the right
4. Start typing your design requests!

### Option 2: PowerShell
```powershell
.\LAUNCHER.ps1
```

### Option 3: Command Line
```cmd
LAUNCHER.bat
```

---

## 📦 What Happens When You Launch

```
1. ✓ Validates add-in structure
2. ✓ Checks for Fusion 360 installation  
3. ✓ Installs add-in to Fusion (automatic)
4. ✓ Launches Fusion 360
5. ✓ Copilot Assistant is ready!
```

---

## 💻 Convert to Windows EXE (Optional)

If you want a standalone `.exe` file:

```powershell
.\Convert-To-EXE.ps1
```

This creates `LAUNCHER.exe` which you can:
- Double-click to launch
- Pin to taskbar
- Send to Start Menu
- Distribute to others

---

## 🎯 Using Copilot Assistant

Once Fusion 360 loads:

### 1️⃣ Access the Panel
- **View** → **Copilot Assistant** (right sidebar)

### 2️⃣ Describe Your Design
Examples:
```
"Create a parametric bracket with 100mm width"
"Add 4x M6 holes in a rectangular pattern"
"Make a 3-axis milling setup"
```

### 3️⃣ Review Generated Code
- See the plan and Fusion Python code
- Click "Explain" for details
- Click "Apply" to execute

### 4️⃣ Iterate
- Results appear instantly
- Use Fusion's undo if needed
- Ask for modifications

---

## 📋 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Send message | `Ctrl+Enter` |
| Focus input | `Ctrl+Shift+K` |
| Undo last action | `Ctrl+Z` |
| Clear chat | `Ctrl+L` |

---

## 🔧 Troubleshooting

### "Fusion 360 Not Found"
- Install from: https://www.autodesk.com/products/fusion-360
- Download Fusion 360 2024+ recommended

### "Add-in not showing"
- **Restart Fusion 360**
- Go to **View** → **Copilot Assistant**
- Check log file: `copilot_launcher.log`

### "Need Admin Rights"
- Right-click `LAUNCHER.bat` → Run as Administrator

### "Port in use" (if using local LLM)
- Ensure Ollama running: http://localhost:11434
- Or switch to OpenAI in Settings

---

## ⚙️ Configuration

### Settings
Open Copilot panel → Click ⚙️ icon

Options:
- **LLM Model**: OpenAI / Ollama / Offline
- **API Key**: Your OpenAI key (if using cloud)
- **Project Root**: Path to your CAD project
- **Auto-run**: Execute code automatically

### Log File
Activity logged to: `copilot_launcher.log`

---

## 📚 Documentation

- **LAUNCHER_GUIDE.md** - Detailed launcher information
- **TESTING.md** - How to run tests
- **fusion_copilot_addin/README.md** - Full technical docs

---

## 🎓 Example Workflows

### Parametric Bracket
```
Input: "Create a parametric bracket 100mm x 50mm x 10mm"
Output: 
  ✓ Created 3 user parameters (Width, Height, Thickness)
  ✓ Sketch on XY plane
  ✓ Extrude with thickness
  ✓ All features named for editing
```

### Edit Existing
```
Input: "Make the walls 2mm thicker"
Output:
  ✓ Detected existing thickness parameter
  ✓ Updated to new value
  ✓ Design recalculated
```

### CAM Setup (Coming Soon)
```
Input: "Create 3-axis face milling setup"
Output:
  ✓ WCS configured
  ✓ Tool selected
  ✓ Feed rates optimized
```

---

## 🤝 Getting Help

**Issues?**
1. Check log: `copilot_launcher.log`
2. Run tests: `.\RUN.ps1`
3. Open GitHub issue: https://github.com/SV-Nikolov/Assist360/issues

**Want to contribute?**
See `CONTRIBUTE.md` or open a pull request

---

## 📊 Current Status

| Feature | Status |
|---------|--------|
| Parametric Parts | ✅ Ready |
| Chat Interface | ✅ Ready |
| Code Execution | ✅ Ready |
| Error Recovery | ✅ Ready |
| OpenAI Integration | 🚧 Phase 2 |
| Ollama Support | 🚧 Phase 2 |
| CAM Generation | 🚧 Phase 3 |
| Drawing Creation | 🚧 Phase 3 |

---

## 📞 Support

**Version**: 0.1.0  
**Last Updated**: February 1, 2026  
**Repository**: https://github.com/SV-Nikolov/Assist360

---

**Ready to create amazing designs? Launch Fusion 360 and start building! 🚀**

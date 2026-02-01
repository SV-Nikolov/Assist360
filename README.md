# Fusion 360 Copilot Assistant 🚀

**AI-powered Copilot-style assistant for Autodesk Fusion 360**

Generate parametric parts, CAM setups, and drawings using natural language. Like GitHub Copilot, but for CAD design.

---

## 🎯 Quick Start

### 1. Launch the Application
**Double-click:** `LAUNCHER.bat`

That's it! The launcher will:
- ✓ Validate the installation
- ✓ Install the add-in to Fusion 360
- ✓ Launch Fusion 360 with Copilot

### 2. Use Copilot
- Wait for Fusion 360 to load
- Look for **"Copilot Assistant"** panel (right sidebar)
- Type: *"Create a parametric bracket 100mm x 50mm"*
- Click **Apply** to generate

### 3. Iterate
- Modify the design with natural language
- Code executes instantly
- Use Fusion undo if needed

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **QUICKSTART.md** | User guide - start here! |
| **LAUNCHER_GUIDE.md** | Detailed launcher documentation |
| **LAUNCHER_SUMMARY.md** | How the launcher works |
| **fusion_copilot_addin/README.md** | Technical documentation |
| **fusion_copilot_addin/ARCHITECTURE.md** | System design |
| **TESTING.md** | How to run tests |

---

## 🛠️ Available Tools

### For Users
- **`LAUNCHER.bat`** - Launch Fusion 360 with Copilot (easiest)
- **`LAUNCHER.ps1`** - PowerShell version with logging

### For Developers
- **`RUN.ps1`** / **`RUN.bat`** - Run validation tests
- **`Convert-To-EXE.ps1`** - Convert launcher to standalone .exe
- **`copilot_launcher.log`** - Activity logs

---

## ✨ Features

### Core (Phase 1 - Ready Now)
- ✅ Chat-based code generation
- ✅ Live Fusion context awareness
- ✅ Safe transaction-based execution
- ✅ Error handling with auto-fix suggestions
- ✅ Professional UI with settings panel

### Coming Soon (Phase 2)
- 🚧 OpenAI GPT-4 integration
- 🚧 Ollama local model support
- 🚧 Offline mode

### Future (Phase 3)
- 📅 CAM operation generation
- 📅 Technical drawing creation
- 📅 Geometry feature detection
- 📅 Vision-based blueprint import

---

## 📋 Example Usage

### Create Parametric Parts
```
Input: "Create a parametric bracket 100mm x 50mm x 10mm"

Output:
✓ Creates 3 user parameters (Width, Height, Thickness)
✓ Sketch on XY plane
✓ Extrude with thickness parameter
✓ All features named for future editing
```

### Modify Existing Design
```
Input: "Make the walls 2mm thicker"

Output:
✓ Detects existing thickness parameter
✓ Updates to new value
✓ Design recalculated instantly
```

### Generate CAM Setups (Coming Soon)
```
Input: "Create a 3-axis milling setup"

Output:
✓ WCS configured
✓ Tools selected
✓ Toolpaths optimized
```

---

## 🏗️ Architecture

```
fusion_copilot_addin/
├── core/                    # AI orchestration
│   ├── orchestrator.py     # Request routing
│   ├── context.py          # Fusion context capture
│   ├── executor.py         # Safe code execution
│   └── codegen.py          # Prompt building
├── ui/                      # Web interface
│   ├── panel.html
│   ├── panel.css
│   └── panel.js
├── tools/                   # Integration tools
│   ├── filesystem.py       # Project scanning
│   ├── geometry_extract.py # Geometry analysis
│   └── vision_extract.py   # Image/PDF extraction
└── scripts/                # Examples & utilities
    ├── examples.py
    └── sandbox_runner.py
```

---

## 🔧 System Requirements

### Minimum
- Windows 10/11
- Fusion 360 2020 or later
- 8 GB RAM
- Internet (optional - offline mode supported)

### Recommended
- Windows 11
- Fusion 360 2024+
- 16 GB RAM
- GPU (if using local LLM)

---

## 🚀 Getting Started

### Step 1: Launch
```bash
LAUNCHER.bat
```

### Step 2: Wait
Fusion 360 loads (30-60 seconds)

### Step 3: Design
Type in the Copilot panel:
- "Create a 100mm cube"
- "Add M6 holes in a 4x4 pattern"
- "Generate a milling setup"

### Step 4: Apply
Click **Apply** to execute code in Fusion

### Step 5: Iterate
Refine with follow-up requests

---

## 📊 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| **Infrastructure** | ✅ Complete | Core modules, UI, testing |
| **LLM Integration** | 🚧 Phase 2 | OpenAI, Ollama support |
| **Code Generation** | ✅ Ready | Prompt templates implemented |
| **Execution** | ✅ Ready | Transaction-based execution |
| **CAM Features** | 📅 Phase 3 | Planned for later |
| **Drawing Creation** | 📅 Phase 3 | Planned for later |

---

## 🧪 Testing

Before committing changes:
```powershell
.\RUN.ps1
```

This validates:
- Project structure
- Python syntax
- Configuration
- Documentation
- All 42 tests must pass

---

## 🛞 Create an EXE File

For distribution without PowerShell dependency:

```powershell
.\Convert-To-EXE.ps1
```

Creates `LAUNCHER.exe` which:
- Works on any Windows system
- Can be pinned to taskbar
- Looks professional
- Requires no setup

---

## 📝 Configuration

Settings stored in Copilot panel:

- **LLM Model**: OpenAI / Ollama / Offline
- **API Key**: Your OpenAI key (optional)
- **Project Root**: Path to CAD files (optional)
- **Auto-run**: Execute code automatically

---

## 🤝 Contributing

Want to help? See **CONTRIBUTE.md** or:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `.\RUN.ps1`
5. Submit a pull request

---

## 📞 Support

### Issues?
1. Check the log: `copilot_launcher.log`
2. Run tests: `.\RUN.ps1`
3. Read docs: `QUICKSTART.md`

### GitHub
https://github.com/SV-Nikolov/Assist360

---

## 📄 License

MIT License - See LICENSE file

---

## 🎓 Learn More

- **[QUICKSTART.md](QUICKSTART.md)** - User guide
- **[LAUNCHER_GUIDE.md](LAUNCHER_GUIDE.md)** - Launcher details
- **[fusion_copilot_addin/README.md](fusion_copilot_addin/README.md)** - Technical docs

---

## 🎉 What's New

**Latest (v0.1.0)** - February 1, 2026
- ✅ Infrastructure complete
- ✅ Core modules implemented
- ✅ Professional UI with settings
- ✅ Error handling & recovery
- ✅ Automated test runner
- ✅ Executable launchers
- ✅ Comprehensive documentation

---

**Ready to design smarter? Double-click LAUNCHER.bat and start building!** 🚀

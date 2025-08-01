# ARRI Clip Recovery Tool

A cross-platform GUI application for recovering ARRI MXF files using the ARRI Reference Tool (art-cmd).

## Features

- 🎬 Simple GUI for MXF file recovery
- 📁 File browser for easy clip selection
- 📊 Progress indication during recovery
- 💾 Automatic output naming (*_recovered.mxf)
- 🖥️ Cross-platform support (macOS, Linux, Windows)

## Quick Start

### Option 1: Use Pre-built Distribution

1. Navigate to the `ARRI_MXF_Recovery_Tool` folder
2. Run the appropriate script:
   - **macOS/Linux**: `./START_RECOVERY_TOOL.sh`
   - **Windows**: `START_RECOVERY_TOOL.bat`

### Option 2: Run from Source

```bash
cd app-design-button-window
python3 main.py
```

### Option 3: Create Fresh Distribution

```bash
./create_distribution.sh
cd ARRI_MXF_Recovery_Tool
./START_RECOVERY_TOOL.sh
```

## Requirements

- Python 3.x with tkinter support
- macOS 14.x/15.x, Ubuntu, Rocky Linux, or Windows
- ARRI Reference Tool (included)

## Usage

1. Launch the application
2. Click "Select Clip" to choose an MXF file
3. Click "Start Recovery" to begin the recovery process
4. The recovered file will be saved as `*_recovered.mxf` in the same directory

## Building Standalone Executable

To create a standalone executable that doesn't require Python:

```bash
cd app-design-button-window
pip install pyinstaller
python3 build_standalone.py
```

## Project Structure

```
arri-clip-recovery-art-cmd-app/
├── app-design-button-window/     # Source code
│   └── main.py                   # GUI application
├── art-cmd_0.4.0_macos_universal/# ARRI tool binaries
├── ARRI_MXF_Recovery_Tool/       # Ready-to-use distribution
└── create_distribution.sh        # Distribution builder
```

## License

This GUI tool is provided as-is. The ARRI Reference Tool (art-cmd) is subject to ARRI's End User License Agreement (see `art-cmd_0.4.0_macos_universal/EULA.txt`).

## Support

For issues with:
- The GUI tool: Create an issue in this repository
- The ARRI Reference Tool: Contact ARRI support

## Acknowledgments

Built using the ARRI Reference Tool CMD version 0.4.0.
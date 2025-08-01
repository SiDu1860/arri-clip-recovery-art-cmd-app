# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains the ARRI Reference Tool Command-line (art-cmd) version and a Python GUI application for ARRI clip recovery. The tool is used for processing ARRI camera footage, including MXF/ProRes files and ARRIRAW/ARRICORE essence containers.

## Project Structure

```
/
├── art-cmd_0.4.0_macos_universal/    # ARRI Reference Tool binary distribution
│   ├── bin/art-cmd                   # Main executable
│   ├── lib/                          # Dynamic libraries and plugins
│   └── doc/                          # Documentation and schemas
├── app-design-button-window/         # Python GUI recovery tool
│   ├── main.py                       # Complete Tkinter-based GUI application
│   ├── run_recovery_tool.sh          # Launch script for macOS/Linux
│   ├── run_recovery_tool.bat         # Launch script for Windows
│   ├── build_standalone.py           # PyInstaller build script
│   └── README.md                     # Application documentation
└── ARRI_MXF_Recovery_Tool/           # Full functional distribution
    ├── main.py                       # GUI application
    ├── START_RECOVERY_TOOL.sh/bat    # Quick launch scripts
    ├── run_recovery_tool.sh/bat      # Alternative launch scripts
    ├── art-cmd/                      # Complete art-cmd with all libs
    ├── README.md                     # Full documentation
    └── QUICK_START.txt               # Quick usage guide
```

## Commands

### ARRI Reference Tool (art-cmd)

The main executable is located at: `./art-cmd_0.4.0_macos_universal/bin/art-cmd`

#### Modes of Operation

1. **process** - Process ARRIRAW/ARRICORE/ProRes clips
   - `art-cmd process --input <path> --output <path>`
   - Outputs: EXR or TIFF files (single frames) or MXF (ProRes)
   - Supports batch processing of directories

2. **trim** - Trim and rewrap clips to RDD 54/55 conformant MXF
   - `art-cmd trim --input <path> --output <path> --start <frame> --duration <frames>`
   - Works with ARRIRAW, ARRICORE, and ProRes clips

3. **export** - Export audio tracks (WAV) and metadata (JSON)
   - `art-cmd export --input <path> --output <path>`
   - Use `--skip-audio` or `--skip-metadata` to export only one type

4. **verify** - Check clip integrity
   - Single clip: `art-cmd verify --input <path>` (checks video frame checksums)
   - Two clips: `art-cmd verify --input <path1> --input <path2>` (compares video/audio/metadata)

5. **mxf-recovery** - Recover unfinalized MXF clips
   - `art-cmd mxf-recovery --input <path>`

#### Key Parameters

**Input/Output:**
- `--input <path>`: Input clip(s) - supports multiple paths, directories, and printf format for sequences
- `--output <path>`: Output path - file or directory (defaults to `./[mode]/`)
- `--start <frame>`: Starting frame (default: 0)
- `--duration <frames>`: Number of frames to process (default: -1 for all)

**Processing Options:**
- `--parameters <file>`: JSON/XML file with ARRIRAW/ARRICORE decoding parameters
- `--target-colorspace <space>`: Output colorspace options include:
  - Linear: 'AP0/D60/linear', 'AWG4/D65/linear', 'AWG3/D65/linear'
  - Log: 'AWG4/D65/LogC4', 'AWG3/D65/LogC3'
  - Display: 'Rec.709/D65/BT.1886', 'P3/D65/PQ', 'Rec.2020/D65/HLG', etc.
- `--video-codec <codec>`: 
  - EXR: 'exr_uncompressed/f16', 'exr_piz/f16', 'exr_zip/f16', etc.
  - ProRes: 'prores422lt', 'prores422', 'prores422hq', 'prores4444', 'prores4444xq'

**Look Management:**
- `--embedded-look`: Apply look embedded in clip
- `--arri-look-file <file>`: Apply external look file (.aml, .alf4, .alf4c)

**Image Transforms:**
- `--deflip`: Apply flip/flop based on camera metadata
- `--desqueeze`: Apply desqueeze based on lens metadata
- `--letterbox-size <width>x<height>`: Apply letterboxing

**Render Platform:**
- `--render-platform <platform>`: 'cpu', 'cuda', 'metal', 'opencl', 'auto' (default: auto)
- `--render-device <index>`: Device index for rendering (default: -1 for best available)

**Utility Options:**
- `--cli <json>`: Batch processing from JSON file defining render queue
- `--verbose <level>`: 'info', 'warning', 'error', 'quiet' (default: info)
- `--logpath <path>`: Log file location (default: art.log)
- `--ls-target-colorspaces`: List available colorspaces for input
- `--ls-devices`: List available rendering devices

### Python GUI Application

The recovery tool GUI is at `app-design-button-window/main.py`. It's a complete Tkinter interface that:
- Provides file selection dialog for MXF files
- Shows selected filename in text field
- Runs art-cmd mxf-recovery in background thread
- Displays progress bar during recovery
- Saves output as *_recovered.mxf in same directory
- Shows success/error dialogs with details

## Architecture

The art-cmd tool is a native macOS universal binary that:
- Processes ARRIRAW and ARRICORE essence containers
- Supports MXF/ProRes reading and writing
- Handles colorspace conversions between LogC3/4, ACES AP0, and AWG colorspaces
- Uses dynamic plugin architecture for transforms (CPU, FMA, Metal, OpenCL)
- Includes JPEG-XS codec support

The Python GUI provides a user-friendly interface specifically for the MXF recovery functionality, with:
- Cross-platform compatibility (macOS, Linux, Windows)
- Automatic art-cmd path detection
- Thread-based processing to keep UI responsive
- Progress indication and status feedback

## Development Notes

- No build system files present - this appears to be a pre-built binary distribution
- Python app requires only standard library (tkinter)
- The art-cmd tool accepts JSON parameter files for complex processing configurations
- Schemas for CLI and parameters are available in doc/ directory
- One distribution script available:
  - `create_distribution.sh` - Full distribution with all necessary files and libraries

## Current Status

### Completed Features
- ✅ GUI application with file selection and recovery functionality
- ✅ Progress bar and status indicators
- ✅ Error handling with user-friendly messages
- ✅ Cross-platform launch scripts
- ✅ Distribution packaging scripts
- ✅ Standalone executable build script (PyInstaller)
- ✅ Comprehensive documentation

### Distribution Package
**ARRI_MXF_Recovery_Tool** - Full functional distribution with all required libraries and plugins. This is the only working distribution that includes all necessary components for the SDK to initialize properly.

### Usage
The tool is ready for deployment. Users can:
1. Run directly with Python: `python3 main.py`
2. Use launch scripts: `./run_recovery_tool.sh` or `run_recovery_tool.bat`
3. Use distribution packages by copying the folder and running START scripts
4. Build standalone executables with `python3 build_standalone.py`

## Repository Information

This project is hosted on GitHub at: https://github.com/SiDu1860/arri-clip-recovery-art-cmd-app

### Clone and Setup
```bash
git clone https://github.com/SiDu1860/arri-clip-recovery-art-cmd-app.git
cd arri-clip-recovery-art-cmd-app
./create_distribution.sh  # Create the full distribution
```

### Repository Structure
- Source code in `app-design-button-window/`
- ARRI tool binaries in `art-cmd_0.4.0_macos_universal/`
- Ready-to-use distribution in `ARRI_MXF_Recovery_Tool/`

Note: The repository includes the ARRI Reference Tool binaries which are subject to ARRI's EULA.
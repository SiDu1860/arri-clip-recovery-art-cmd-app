# ARRI MXF Recovery Tool

A cross-platform GUI application for recovering ARRI MXF files using the art-cmd tool.

## Features

- Simple, user-friendly interface
- File browser for selecting MXF files
- Progress indication during recovery
- Automatic output naming (*_recovered.mxf)
- Cross-platform support (macOS, Linux, Windows)

## Requirements

- Python 3.x (with tkinter)
- art-cmd tool (included in parent directory)

## Running the Tool

### Option 1: Using Launch Scripts

**macOS/Linux:**
```bash
./run_recovery_tool.sh
```

**Windows:**
```batch
run_recovery_tool.bat
```

### Option 2: Direct Python Execution
```bash
python3 main.py
```

## Building Standalone Executable

To create a standalone executable that doesn't require Python installation:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python3 build_standalone.py
   ```

3. The executable will be created in the `dist` folder

## Usage

1. Launch the application
2. Click "Select Clip" button
3. Browse and select the MXF file you want to recover
4. The selected file path will appear in the text field
5. Click "Start Recovery" to begin the recovery process
6. A progress bar will show during processing
7. Upon completion, you'll see a success message with the output file location

## Output

Recovered files are saved in the same directory as the input file with `_recovered.mxf` suffix.

Example:
- Input: `/path/to/clip.mxf`
- Output: `/path/to/clip_recovered.mxf`

## Troubleshooting

### "art-cmd not found" Error
Make sure the art-cmd executable is in one of these locations:
- `../art-cmd_0.4.0_macos_universal/bin/art-cmd`
- `../art-cmd/bin/art-cmd`
- `../bin/art-cmd`
- System PATH

### GUI Not Launching
Ensure Python has tkinter support:
```bash
python3 -m tkinter
```

### Recovery Fails
Check the error message dialog for details. Common issues:
- Corrupted MXF file beyond recovery
- Insufficient permissions
- Disk space issues

## Platform Notes

### macOS
- Tested on macOS 14.x and 15.x
- Requires Python 3 with tkinter (usually pre-installed)

### Linux (Ubuntu/Rocky)
- May need to install tkinter: `sudo apt-get install python3-tk`
- Ensure art-cmd has execute permissions

### Windows
- Python installation should include tkinter by default
- Use `.exe` version of art-cmd
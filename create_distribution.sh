#!/bin/bash
# Script to create a clean distribution folder with only necessary files

echo "Creating ARRI MXF Recovery Tool distribution..."

# Set paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIST_NAME="ARRI_MXF_Recovery_Tool"
DIST_DIR="$SCRIPT_DIR/$DIST_NAME"

# Remove old distribution if exists
if [ -d "$DIST_DIR" ]; then
    echo "Removing old distribution folder..."
    rm -rf "$DIST_DIR"
fi

# Create distribution directory
echo "Creating distribution folder: $DIST_NAME"
mkdir -p "$DIST_DIR"

# Copy the Python application
echo "Copying application files..."
cp "$SCRIPT_DIR/app-design-button-window/main.py" "$DIST_DIR/"
cp "$SCRIPT_DIR/app-design-button-window/run_recovery_tool.sh" "$DIST_DIR/"
cp "$SCRIPT_DIR/app-design-button-window/run_recovery_tool.bat" "$DIST_DIR/"
cp "$SCRIPT_DIR/app-design-button-window/README.md" "$DIST_DIR/"

# Make shell script executable
chmod +x "$DIST_DIR/run_recovery_tool.sh"

# Copy art-cmd binary and required libraries
echo "Copying art-cmd tool..."
mkdir -p "$DIST_DIR/art-cmd/bin"
cp "$SCRIPT_DIR/art-cmd_0.4.0_macos_universal/bin/art-cmd" "$DIST_DIR/art-cmd/bin/"
chmod +x "$DIST_DIR/art-cmd/bin/art-cmd"

# Copy ALL libraries and plugins (required for SDK initialization)
echo "Copying all required libraries and plugins..."
mkdir -p "$DIST_DIR/art-cmd/lib"
# Copy all libraries
cp -r "$SCRIPT_DIR/art-cmd_0.4.0_macos_universal/lib/"* "$DIST_DIR/art-cmd/lib/" 2>/dev/null || true

# Copy documentation (minimal)
echo "Copying documentation..."
mkdir -p "$DIST_DIR/art-cmd/doc"
cp "$SCRIPT_DIR/art-cmd_0.4.0_macos_universal/doc/USAGE.md" "$DIST_DIR/art-cmd/doc/" 2>/dev/null || true

# Create a simple start script at the root
cat > "$DIST_DIR/START_RECOVERY_TOOL.sh" << 'EOF'
#!/bin/bash
# Quick start script for ARRI MXF Recovery Tool

cd "$(dirname "$0")"
./run_recovery_tool.sh
EOF

chmod +x "$DIST_DIR/START_RECOVERY_TOOL.sh"

# Create a simple start script for Windows
cat > "$DIST_DIR/START_RECOVERY_TOOL.bat" << 'EOF'
@echo off
REM Quick start script for ARRI MXF Recovery Tool

cd /d "%~dp0"
call run_recovery_tool.bat
EOF

# Create a simplified README at the root
cat > "$DIST_DIR/QUICK_START.txt" << 'EOF'
ARRI MXF Recovery Tool - Quick Start
====================================

TO RUN THE TOOL:

macOS/Linux:
  Double-click: START_RECOVERY_TOOL.sh
  Or in Terminal: ./START_RECOVERY_TOOL.sh

Windows:
  Double-click: START_RECOVERY_TOOL.bat

USAGE:
1. Click "Select Clip" to choose an MXF file
2. Click "Start Recovery" to recover the file
3. Recovered file will be saved as *_recovered.mxf

REQUIREMENTS:
- Python 3 with tkinter (usually pre-installed on macOS)
- For Linux: may need to install python3-tk package

For detailed information, see README.md
EOF

echo ""
echo "Distribution created successfully!"
echo "Location: $DIST_DIR"
echo ""
echo "Contents:"
ls -la "$DIST_DIR"
echo ""
echo "The folder '$DIST_NAME' contains everything needed to run the recovery tool."
echo "You can move or copy this folder anywhere."
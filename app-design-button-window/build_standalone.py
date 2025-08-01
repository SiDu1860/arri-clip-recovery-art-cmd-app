#!/usr/bin/env python3
"""
Build standalone executables for ARRI MXF Recovery Tool
Supports: macOS, Linux (Ubuntu/Rocky), Windows
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def build_executable():
    """Build standalone executable for current platform"""
    if not check_pyinstaller():
        print("Failed to install PyInstaller")
        return False
    
    # Determine platform-specific settings
    system = platform.system()
    
    # Base PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Single file executable
        "--windowed",  # No console window
        "--name", "ARRI_MXF_Recovery",
        "--distpath", "./dist",
        "--workpath", "./build",
        "--specpath", "./build",
    ]
    
    # Platform-specific options
    if system == "Darwin":  # macOS
        cmd.extend([
            "--osx-bundle-identifier", "com.arri.mxfrecovery",
            "--icon", "icon.icns" if Path("icon.icns").exists() else None,
        ])
    elif system == "Windows":
        cmd.extend([
            "--icon", "icon.ico" if Path("icon.ico").exists() else None,
            "--version-file", "version.txt" if Path("version.txt").exists() else None,
        ])
    elif system == "Linux":
        cmd.extend([
            "--icon", "icon.png" if Path("icon.png").exists() else None,
        ])
    
    # Remove None values
    cmd = [c for c in cmd if c is not None]
    
    # Add the main script
    cmd.append("main.py")
    
    print(f"Building for {system}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild successful!")
        
        # Find the output file
        if system == "Windows":
            exe_name = "ARRI_MXF_Recovery.exe"
        else:
            exe_name = "ARRI_MXF_Recovery"
        
        exe_path = Path("dist") / exe_name
        
        if exe_path.exists():
            print(f"Executable created: {exe_path}")
            print(f"File size: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
            
            # Create distribution package
            create_distribution(exe_path, system)
        else:
            print("Error: Executable not found!")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    
    return True

def create_distribution(exe_path, system):
    """Create a distribution package with art-cmd included"""
    dist_name = f"ARRI_MXF_Recovery_{system}"
    dist_dir = Path("dist") / dist_name
    
    # Create distribution directory
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    shutil.copy2(exe_path, dist_dir)
    
    # Copy art-cmd directory structure
    art_cmd_src = Path("..") / "art-cmd_0.4.0_macos_universal"
    if art_cmd_src.exists():
        art_cmd_dst = dist_dir / "art-cmd"
        print(f"Copying art-cmd from {art_cmd_src} to {art_cmd_dst}")
        shutil.copytree(art_cmd_src, art_cmd_dst, dirs_exist_ok=True)
    
    # Create README
    readme_content = f"""ARRI MXF Recovery Tool
====================

This tool provides a simple GUI for recovering ARRI MXF files.

Usage:
1. Double-click the ARRI_MXF_Recovery executable
2. Click "Select Clip" to choose an MXF file
3. Click "Start Recovery" to begin the recovery process
4. The recovered file will be saved as *_recovered.mxf in the same directory

Requirements:
- {system} operating system
- No installation required

Note: The art-cmd directory must be in the same location as this executable.

Version: 1.0.0
"""
    
    with open(dist_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    # Create archive
    if system == "Windows":
        archive_name = f"{dist_name}.zip"
        shutil.make_archive(str(dist_dir), 'zip', dist_dir)
    else:
        archive_name = f"{dist_name}.tar.gz"
        shutil.make_archive(str(dist_dir), 'gztar', dist_dir)
    
    print(f"\nDistribution package created: dist/{archive_name}")

def create_spec_file():
    """Create a custom spec file for more control"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ARRI_MXF_Recovery',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    with open("ARRI_MXF_Recovery.spec", "w") as f:
        f.write(spec_content)

if __name__ == "__main__":
    print("ARRI MXF Recovery Tool - Standalone Builder")
    print("=" * 50)
    
    # Clean previous builds
    for path in ["build", "dist", "__pycache__"]:
        if Path(path).exists():
            shutil.rmtree(path)
    
    # Build executable
    if build_executable():
        print("\nBuild completed successfully!")
        print("\nTo distribute:")
        print("1. Test the executable in the dist folder")
        print("2. Share the distribution package from the dist folder")
    else:
        print("\nBuild failed!")
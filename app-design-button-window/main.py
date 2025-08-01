#!/usr/bin/env python3
"""
ARRI MXF Recovery Tool
A cross-platform GUI tool for recovering ARRI MXF files using art-cmd
"""

import os
import sys
import platform
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

class MXFRecoveryTool:
    def __init__(self, root):
        self.root = root
        self.root.title("ARRI Reference Tool - CMD - Recovery Tool")
        self.root.config(bg="#005ca5")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Variables
        self.selected_file = tk.StringVar()
        self.is_processing = False
        
        # Find art-cmd executable
        self.art_cmd_path = self.find_art_cmd()
        
        # Create widgets
        self.create_widgets()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def find_art_cmd(self):
        """Find the art-cmd executable based on the platform"""
        base_dir = Path(__file__).parent
        
        # Check common locations
        possible_paths = [
            base_dir / "art-cmd" / "bin" / "art-cmd",  # Distribution structure
            base_dir.parent / "art-cmd_0.4.0_macos_universal" / "bin" / "art-cmd",  # Development structure
            base_dir.parent / "art-cmd" / "bin" / "art-cmd",
            base_dir / "bin" / "art-cmd",
            Path("./art-cmd"),
        ]
        
        # Add .exe extension for Windows
        if platform.system() == "Windows":
            possible_paths = [p.with_suffix(".exe") if not p.suffix else p for p in possible_paths]
        
        for path in possible_paths:
            if path.exists() and path.is_file():
                return str(path)
                
        # If not found, assume it's in PATH
        return "art-cmd"
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # File selection frame
        file_frame = tk.Frame(self.root, bg="#005ca5")
        file_frame.pack(pady=20)
        
        # Entry field for file path
        self.entry = tk.Entry(
            file_frame,
            textvariable=self.selected_file,
            bg="#505050",
            fg="#ffffff",
            relief=tk.FLAT,
            width=30,
            font=("Arial", 10)
        )
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Select button
        self.select_button = tk.Button(
            file_frame,
            text="Select Clip",
            command=self.select_file,
            bg="#505050",
            fg="#ffffff",
            relief=tk.FLAT,
            font=("Arial", 10),
            padx=15,
            pady=5
        )
        self.select_button.pack(side=tk.LEFT)
        
        # Start recovery button
        self.start_button = tk.Button(
            self.root,
            text="Start Recovery",
            command=self.start_recovery,
            bg="#505050",
            fg="#ffffff",
            relief=tk.FLAT,
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            state=tk.DISABLED
        )
        self.start_button.pack(pady=10)
        
        # Progress bar (initially hidden)
        self.progress_frame = tk.Frame(self.root, bg="#005ca5")
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=300
        )
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Processing...",
            bg="#005ca5",
            fg="#ffffff",
            font=("Arial", 9)
        )
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="",
            bg="#005ca5",
            fg="#ffffff",
            font=("Arial", 9)
        )
        self.status_label.pack(pady=5)
        
    def select_file(self):
        """Open file dialog to select MXF file"""
        filename = filedialog.askopenfilename(
            title="Select MXF file to recover",
            filetypes=[("MXF files", "*.mxf"), ("All files", "*.*")]
        )
        
        if filename:
            self.selected_file.set(filename)
            self.start_button.config(state=tk.NORMAL)
            self.status_label.config(text=f"Selected: {Path(filename).name}")
            
    def start_recovery(self):
        """Start the recovery process in a separate thread"""
        if self.is_processing:
            return
            
        input_path = self.selected_file.get()
        if not input_path or not Path(input_path).exists():
            messagebox.showerror("Error", "Please select a valid MXF file")
            return
            
        # Disable buttons and show progress
        self.is_processing = True
        self.select_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.show_progress()
        
        # Start recovery in background thread
        thread = threading.Thread(target=self.run_recovery, args=(input_path,))
        thread.daemon = True
        thread.start()
        
    def show_progress(self):
        """Show progress bar and label"""
        self.progress_frame.pack(pady=10)
        self.progress_bar.pack()
        self.progress_label.pack(pady=5)
        self.progress_bar.start(10)
        self.status_label.config(text="")
        
    def hide_progress(self):
        """Hide progress bar and label"""
        self.progress_bar.stop()
        self.progress_frame.pack_forget()
        
    def run_recovery(self, input_path):
        """Run the art-cmd recovery process"""
        try:
            # Prepare output path
            input_file = Path(input_path)
            output_path = input_file.parent / f"{input_file.stem}_recovered.mxf"
            
            # Update progress label
            self.root.after(0, lambda: self.progress_label.config(text=f"Recovering {input_file.name}..."))
            
            # Build command
            cmd = [
                self.art_cmd_path,
                "mxf-recovery",
                "--input", str(input_path),
                "--output", str(output_path),
                "--verbose", "info"
            ]
            
            # Run the command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True
            )
            
            # Monitor the process
            stdout, stderr = process.communicate()
            
            # Check result
            if process.returncode == 0:
                self.root.after(0, lambda: self.recovery_success(output_path))
            else:
                error_msg = stderr if stderr else "Unknown error occurred"
                self.root.after(0, lambda: self.recovery_failed(error_msg))
                
        except FileNotFoundError:
            self.root.after(0, lambda: self.recovery_failed(
                f"art-cmd not found at {self.art_cmd_path}\n"
                "Please ensure art-cmd is in the correct location."
            ))
        except Exception as e:
            self.root.after(0, lambda: self.recovery_failed(str(e)))
            
    def recovery_success(self, output_path):
        """Handle successful recovery"""
        self.hide_progress()
        self.is_processing = False
        self.select_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        
        self.status_label.config(text=f"✓ Recovery successful: {Path(output_path).name}")
        messagebox.showinfo(
            "Success",
            f"MXF file recovered successfully!\n\nOutput: {output_path}"
        )
        
    def recovery_failed(self, error_msg):
        """Handle failed recovery"""
        self.hide_progress()
        self.is_processing = False
        self.select_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        
        self.status_label.config(text="✗ Recovery failed")
        messagebox.showerror(
            "Recovery Failed",
            f"Failed to recover MXF file:\n\n{error_msg}"
        )

def main():
    """Main entry point"""
    root = tk.Tk()
    app = MXFRecoveryTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
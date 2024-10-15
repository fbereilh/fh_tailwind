# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['run_command', 'check_node_installed', 'setup_tailwind', 'update_styles']

# %% ../nbs/00_core.ipynb 3
import re
import os
import shutil
from pathlib import Path
import subprocess
import sys

# %% ../nbs/00_core.ipynb 4
def run_command(command, cwd=None):
    """Utility function to run shell commands."""
    process = subprocess.Popen(command, shell=True, cwd=cwd)
    process.communicate()


# %% ../nbs/00_core.ipynb 6
def check_node_installed():
    """Check if Node.js is installed and accessible in the PATH."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
        print(f"Node.js is installed. Version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Node.js is required but not installed or not found in PATH.")
        print("Please install Node.js from https://nodejs.org/")
        sys.exit(1)

# %% ../nbs/00_core.ipynb 8
def setup_tailwind():
    """Install and configure Tailwind CSS and DaisyUI in the node directory."""
    # Check if Node.js is installed
    check_node_installed()

    root_dir = Path.cwd()
    node_dir = root_dir / 'node'
    public_dir = root_dir / 'public'
    
    # Create necessary folders
    public_dir.mkdir(parents=True, exist_ok=True)
    node_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Initialize Node.js and Install Tailwind CSS and DaisyUI
    print("Initializing Node.js project and installing Tailwind CSS and DaisyUI...")
    run_command('npm init -y', cwd=node_dir)
    run_command('npm install tailwindcss@3.4.13 daisyui@4.12.13', cwd=node_dir)

    print("Creating Tailwind configuration file with custom theme...")
    tailwind_config_path = node_dir / 'tailwind.config.js'
    
    tailwind_config_content = """
module.exports = {
  content: ["./extracted_classes.html"],
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        "mytheme": {
          "primary": "#a2d7db",
          "secondary": "#fede80",
          "accent": "#f0938e",
          "neutral": "#d8d8d8",
          "base-100": "#ebebeb",
          "info": "#0ea5e9",
          "success": "#22c55e",
          "warning": "#eab308",
          "error": "#ef4444",
          "--rounded-box": "1rem",
          "--rounded-btn": "0.5rem",
          "--rounded-badge": "1.9rem",
          "--animation-btn": "0.25s",
          "--animation-input": "0.2s",
          "--btn-focus-scale": "0.95",
          "--border-btn": "1px",
          "--tab-border": "1px",
          "--tab-radius": "0.5rem",
        },
      },
      "light", "dark"
    ],
  },
}
"""
    with tailwind_config_path.open('w') as f:
        f.write(tailwind_config_content)

    # Step 3: Create a CSS file to define Tailwind CSS setup
    print("Creating Tailwind input CSS file in the node directory...")
    tailwind_css_path = node_dir / 'tailwind.css'
    tailwind_css_content = """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  /* You can add your custom component styles here */
}
"""
    with tailwind_css_path.open('w') as f:
        f.write(tailwind_css_content)
        
    # Step 5: Create a .gitignore file to exclude node_modules
    print("Creating .gitignore file in the node directory...")
    gitignore_path = node_dir / '.gitignore'
    gitignore_content = "node_modules/"
    with gitignore_path.open('w') as f:
        f.write(gitignore_content)

    # Step 4: Build Tailwind CSS Once, Output to the Public Directory
    print("Building Tailwind CSS...")
    output_css_path = public_dir / 'styles.css'
    run_command(f'npx tailwindcss -i tailwind.css -o {output_css_path}', cwd=node_dir)

    print("Tailwind CSS and DaisyUI setup is complete!")




# %% ../nbs/00_core.ipynb 11
def update_styles():
    """Extract Tailwind CSS classes from dynamic Python components and update Tailwind setup.
    """
    project_root = Path.cwd()  # Get the current working directory
    python_files = list(project_root.glob("**/*.py"))  # Find all Python files in the project

    all_classes = set()  # Set to hold unique class names

    # Regular expression to match cls="..." patterns
    class_pattern = re.compile(r"cls=['\"]([^'\"]+)['\"]")

    # Loop through all Python files and extract classes
    for file in python_files:
        with file.open() as f:
            content = f.read()
            matches = class_pattern.findall(content)
            for match in matches:
                # Split class strings into individual class names and add to the set
                all_classes.update(match.split())

    # Create an HTML file containing all the classes for Tailwind to scan
    node_dir = project_root / "node"
    extracted_classes_file = node_dir / "extracted_classes.html"
    extracted_classes_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure the node folder exists

    with extracted_classes_file.open("w") as output:
        for cls in all_classes:
            output.write(f"<div class='{cls}'></div>\n")

    print(f"Classes extracted to '{extracted_classes_file}'.")

    # Run Tailwind CSS build or watch based on the 'watch' parameter
    public_dir = project_root / 'public'
    output_css_path = public_dir / 'styles.css'
    input_css_path = project_root / 'node/tailwind.css'


    print("Building styles.css...")
    run_command(f'npx tailwindcss -i {input_css_path} -o {output_css_path}', cwd=node_dir)

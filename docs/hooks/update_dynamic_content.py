#!/usr/bin/env python3
"""
MkDocs hook to update dynamic content before building documentation.
This ensures parameter documentation and version info are always current.
"""

import json
import subprocess
from pathlib import Path


def on_pre_build(config, **kwargs):
    """
    Hook that runs before MkDocs builds the documentation.
    Regenerates parameter documentation from nextflow_schema.json.
    """
    print("🔄 Updating dynamic documentation content...")
    
    # Get project root (assuming docs/hooks/ structure)
    project_root = Path(__file__).parent.parent.parent
    
    # Run the parameter documentation generator
    script_path = project_root / 'bin' / 'generate_parameter_docs.py'
    
    if script_path.exists():
        try:
            result = subprocess.run(
                ['python3', str(script_path)],
                capture_output=True,
                text=True,
                cwd=str(project_root)
            )
            
            if result.returncode == 0:
                print("✅ Parameter documentation updated successfully")
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"⚠️  Warning: Failed to update parameter documentation")
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"⚠️  Warning: Could not run parameter generator: {e}")
    else:
        print(f"⚠️  Warning: Parameter generator script not found at {script_path}")
    
    # Update version information
    update_version_info(project_root)
    
    print("✅ Dynamic content update complete")


def update_version_info(project_root):
    """
    Update version information in documentation from nextflow.config.
    """
    config_path = project_root / 'nextflow.config'
    version_file = project_root / 'docs' / '.version'
    
    if not config_path.exists():
        print("⚠️  Warning: nextflow.config not found")
        return
    
    try:
        # Extract version from nextflow.config
        with open(config_path, 'r') as f:
            for line in f:
                if 'version' in line and '=' in line:
                    # Extract version string (e.g., version = '1.0.0')
                    parts = line.split('=')
                    if len(parts) == 2:
                        version = parts[1].strip().strip("'\"")
                        
                        # Write to .version file for use in templates
                        with open(version_file, 'w') as vf:
                            vf.write(version)
                        
                        print(f"📌 Pipeline version: {version}")
                        break
    except Exception as e:
        print(f"⚠️  Warning: Could not extract version: {e}")


def on_page_markdown(markdown, page, config, files):
    """
    Hook to modify page markdown before rendering.
    Adds dynamic content like version numbers.
    """
    project_root = Path(__file__).parent.parent.parent
    version_file = project_root / 'docs' / '.version'
    
    # Replace {{VERSION}} placeholder with actual version
    if version_file.exists():
        with open(version_file, 'r') as f:
            version = f.read().strip()
            markdown = markdown.replace('{{VERSION}}', version)
    
    return markdown

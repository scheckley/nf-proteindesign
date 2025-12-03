#!/usr/bin/env python3
"""
Generate parameter documentation from nextflow_schema.json
This script creates markdown documentation that can be included in MkDocs.
"""

import json
import sys
from pathlib import Path


def load_schema(schema_path):
    """Load the Nextflow schema JSON file."""
    with open(schema_path, 'r') as f:
        return json.load(f)


def format_parameter(key, param_info):
    """Format a single parameter for markdown documentation."""
    param_type = param_info.get('type', 'unknown')
    default = param_info.get('default', 'null')
    description = param_info.get('description', 'No description')
    
    # Format default value
    if default is None or default == '':
        default_str = '`null`'
    elif isinstance(default, bool):
        default_str = f'`{str(default).lower()}`'
    elif isinstance(default, str):
        default_str = f'`"{default}"`'
    else:
        default_str = f'`{default}`'
    
    # Build the parameter entry
    lines = [
        f"### `--{key}`",
        "",
        description,
        "",
        f"- **Type**: `{param_type}`",
        f"- **Default**: {default_str}",
    ]
    
    # Add enum values if present
    if 'enum' in param_info:
        enum_values = ', '.join(f'`{v}`' for v in param_info['enum'])
        lines.append(f"- **Allowed values**: {enum_values}")
    
    # Add pattern if present
    if 'pattern' in param_info:
        lines.append(f"- **Pattern**: `{param_info['pattern']}`")
    
    lines.append("")
    return '\n'.join(lines)


def generate_docs(schema, output_path):
    """Generate complete parameter documentation."""
    definitions = schema.get('definitions', {})
    
    # Start with header
    content = [
        "# Pipeline Parameters",
        "",
        "!!! tip \"Auto-Generated Documentation\"",
        "    This page is automatically generated from `nextflow_schema.json`. ",
        "    Parameter defaults and descriptions reflect the current pipeline version.",
        "",
        "## Overview",
        "",
        f"**Pipeline**: {schema.get('title', 'nf-proteindesign')}",
        f"",
        f"{schema.get('description', '')}",
        "",
    ]
    
    # Process each parameter group
    for group_name, group_info in definitions.items():
        if 'properties' not in group_info:
            continue
            
        # Add group header
        title = group_info.get('title', group_name.replace('_', ' ').title())
        description = group_info.get('description', '')
        
        content.append(f"## {title}")
        content.append("")
        if description:
            content.append(description)
            content.append("")
        
        # Add parameters in this group
        properties = group_info.get('properties', {})
        required = group_info.get('required', [])
        
        for param_key, param_info in properties.items():
            # Mark required parameters
            if param_key in required:
                param_info['description'] = f"**Required.** {param_info.get('description', '')}"
            
            content.append(format_parameter(param_key, param_info))
    
    # Add parameter table summary at the end
    content.extend([
        "---",
        "",
        "## Quick Reference Table",
        "",
        "| Parameter | Type | Default | Description |",
        "|-----------|------|---------|-------------|",
    ])
    
    for group_name, group_info in definitions.items():
        if 'properties' not in group_info:
            continue
        properties = group_info.get('properties', {})
        for param_key, param_info in properties.items():
            param_type = param_info.get('type', 'unknown')
            default = param_info.get('default', 'null')
            if default is None or default == '':
                default = 'null'
            elif isinstance(default, bool):
                default = str(default).lower()
            elif isinstance(default, str):
                default = f'"{default}"'
            desc = param_info.get('description', '').split('.')[0]  # First sentence only
            if len(desc) > 50:
                desc = desc[:47] + "..."
            content.append(f"| `--{param_key}` | `{param_type}` | `{default}` | {desc} |")
    
    content.append("")
    
    # Write to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Generated parameter documentation: {output_path}")


def main():
    # Determine paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    schema_path = project_dir / 'nextflow_schema.json'
    output_path = project_dir / 'docs' / 'reference' / 'parameters.md'
    
    # Load schema and generate docs
    print(f"📖 Reading schema: {schema_path}")
    schema = load_schema(schema_path)
    
    print(f"📝 Generating documentation...")
    generate_docs(schema, output_path)
    
    print(f"✅ Done! Documentation written to: {output_path}")


if __name__ == '__main__':
    main()

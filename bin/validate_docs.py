#!/usr/bin/env python3
"""
Validate documentation structure and mermaid diagrams.
"""

import re
import sys
from pathlib import Path


def validate_mermaid_syntax(file_path, content):
    """
    Basic validation of mermaid diagram syntax.
    """
    errors = []
    
    # Find all mermaid blocks
    mermaid_blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
    
    for i, block in enumerate(mermaid_blocks, 1):
        # Check for common syntax issues
        lines = block.strip().split('\n')
        
        if not lines:
            errors.append(f"Empty mermaid block #{i}")
            continue
        
        # Check first line for diagram type
        first_line = lines[0].strip()
        valid_types = ['graph', 'flowchart', 'sequenceDiagram', 'classDiagram', 'stateDiagram']
        
        if not any(first_line.startswith(t) for t in valid_types):
            errors.append(f"Block #{i}: Invalid or missing diagram type (found: '{first_line}')")
        
        # Check for balanced brackets
        open_brackets = block.count('[') + block.count('{') + block.count('(')
        close_brackets = block.count(']') + block.count('}') + block.count(')')
        
        if open_brackets != close_brackets:
            errors.append(f"Block #{i}: Unbalanced brackets ({open_brackets} open vs {close_brackets} close)")
        
        # Check for arrows in flowcharts
        if first_line.startswith(('graph', 'flowchart')):
            if '-->' not in block and '---' not in block and '==>' not in block:
                errors.append(f"Block #{i}: No arrows found in flowchart")
    
    return errors


def validate_markdown_file(file_path):
    """
    Validate a markdown file for common issues.
    """
    print(f"📄 Checking: {file_path.relative_to(file_path.parents[2])}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    errors = []
    warnings = []
    
    # Check for mermaid diagrams
    if '```mermaid' in content:
        mermaid_errors = validate_mermaid_syntax(file_path, content)
        errors.extend(mermaid_errors)
    
    # Check for broken internal links (basic check)
    internal_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md[^)]*)\)', content)
    for link_text, link_path in internal_links:
        # Remove anchor if present
        clean_path = link_path.split('#')[0]
        
        # Resolve relative path
        if clean_path.startswith('/'):
            target = file_path.parents[1] / clean_path.lstrip('/')
        elif clean_path.startswith('../'):
            target = (file_path.parent / clean_path).resolve()
        else:
            target = file_path.parent / clean_path
        
        if not target.exists():
            warnings.append(f"Possibly broken link: [{link_text}]({link_path})")
    
    # Report results
    if errors:
        print(f"  ❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"     • {error}")
    
    if warnings:
        print(f"  ⚠️  Found {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"     • {warning}")
    
    if not errors and not warnings:
        print(f"  ✅ No issues found")
    
    return len(errors) == 0


def main():
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'
    
    if not docs_dir.exists():
        print(f"❌ Documentation directory not found: {docs_dir}")
        sys.exit(1)
    
    print("🔍 Validating documentation files...\n")
    
    # Find all markdown files
    md_files = list(docs_dir.rglob('*.md'))
    
    if not md_files:
        print("⚠️  No markdown files found!")
        sys.exit(1)
    
    print(f"Found {len(md_files)} markdown file(s)\n")
    
    # Validate each file
    all_valid = True
    for md_file in sorted(md_files):
        # Skip README in hooks directory
        if 'hooks' in md_file.parts:
            continue
        
        if not validate_markdown_file(md_file):
            all_valid = False
        print()  # Blank line between files
    
    # Summary
    print("=" * 60)
    if all_valid:
        print("✅ All documentation files validated successfully!")
        return 0
    else:
        print("❌ Some files have errors. Please fix them before deploying.")
        return 1


if __name__ == '__main__':
    sys.exit(main())

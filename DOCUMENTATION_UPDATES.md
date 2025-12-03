# Documentation Updates Summary

**Date**: 2025-12-02  
**Pipeline Version**: 1.0.0

## Overview

This document summarizes the comprehensive updates made to the nf-proteindesign MkDocs documentation to reflect the current pipeline version and implement dynamic content generation.

## Key Changes

### 1. ✅ Updated Mermaid Workflow Diagrams

All workflow diagrams have been updated to accurately reflect the current pipeline implementation:

#### **docs/index.md**
- **Before**: Simple linear workflow with unclear analysis dependencies
- **After**: Comprehensive workflow showing:
  - Boltzgen precomputed results support
  - Clear branching logic (ProteinMPNN → Boltz-2 → Analysis)
  - All output paths (Boltzgen-only, MPNN-only, Full analysis)
  - Analysis module requirements clearly marked

#### **docs/architecture/design.md**
- **Before**: Showed analysis modules processing both Boltzgen and Boltz-2 outputs
- **After**: Accurate detailed flowchart with:
  - GPU/CPU process labels
  - Data node highlighting
  - All intermediate steps (PREPARE_BOLTZ2_SEQUENCES, etc.)
  - Explicit requirement that analysis modules ONLY process Boltz-2 outputs
  - Precomputed Boltzgen results branching

#### **docs/analysis/proteinmpnn-boltz2.md**
- **Before**: Basic linear workflow
- **After**: Detailed sequential workflow showing:
  - Parallel processing per budget design
  - Multi-FASTA splitting process
  - Target sequence preparation
  - Clear GPU/CPU labels
  - Analysis module integration

### 2. ✅ Implemented Dynamic Content Generation

#### **Auto-Generated Parameter Documentation**
Created `bin/generate_parameter_docs.py` to automatically generate `docs/reference/parameters.md` from `nextflow_schema.json`:

- **Extracts**: Types, defaults, descriptions, enums, patterns
- **Generates**: Structured markdown with sections for each parameter group
- **Includes**: Quick reference table for all parameters
- **Updates**: Automatically on each documentation build

#### **MkDocs Pre-Build Hook**
Created `docs/hooks/update_dynamic_content.py` to:

- Run parameter documentation generator before each build
- Extract and display pipeline version from `nextflow.config`
- Ensure documentation always reflects current schema

### 3. ✅ Corrected Technical Content

#### **Process Table Updates**
- Removed obsolete processes (EXTRACT_TARGET_SEQUENCES, CONVERT_PROTENIX_TO_NPZ)
- Added current processes (PREPARE_BOLTZ2_SEQUENCES)
- Corrected process labels and outputs
- Added dependency information

#### **Module Structure**
- Updated file tree to show actual module organization
- Added assets/ directory with helper scripts
- Documented placeholder files for Kubernetes compatibility

#### **Parameter Documentation**
- Fixed broken internal links (proteinmpnn-protenix → proteinmpnn-boltz2)
- Updated default values to match nextflow.config
- Clarified GPU requirements for all GPU processes

### 4. ✅ Enhanced Visual Design

#### **Color Scheme**
Applied consistent color coding across all diagrams:

```
Primary Purple:   #9C27B0 (Boltzgen process)
Lighter Purple:   #8E24AA (ProteinMPNN process)
Medium Purple:    #7B1FA2 (Boltz-2 process)
Dark Purple:      #6A1B9A (Consolidation process)

GPU Process:      #E1BEE7 fill (light purple)
CPU Process:      #F3E5F5 fill (very light purple)
Data Nodes:       #FFF9C4 fill (yellow)
Decision Nodes:   #FFF3E0 fill (orange tint)
```

#### **Badges**
Added informative badges to `docs/index.md`:

- Version badge (v1.0.0)
- Nextflow DSL2 requirement
- Docker support
- GPU requirement (new!)

### 5. ✅ Added Documentation Maintenance Guide

Created `docs/README.md` with:

- Complete documentation structure overview
- Instructions for updating workflow diagrams
- Mermaid diagram best practices and color codes
- Explanation of dynamic content system
- Tips for documentation writers
- Build and preview instructions

### 6. ✅ Created Validation Tools

#### **Documentation Validator**
`bin/validate_docs.py` checks for:

- Mermaid diagram syntax errors
- Unbalanced brackets in diagrams
- Missing diagram types
- Broken internal links
- Common markdown issues

Run with:
```bash
python3 bin/validate_docs.py
```

## Files Modified

### Updated Files
- `docs/index.md` - Main workflow diagram, badges
- `docs/architecture/design.md` - Complete architecture flowchart, process table, module structure
- `docs/analysis/proteinmpnn-boltz2.md` - Detailed workflow diagram
- `mkdocs.yml` - Added hooks configuration
- `docs/getting-started/installation.md` - Fixed broken links
- `docs/getting-started/quick-reference.md` - Fixed broken links
- `docs/quick-start.md` - Fixed broken links
- `docs/reference/examples.md` - Fixed broken links

### New Files
- `bin/generate_parameter_docs.py` - Parameter doc generator
- `docs/hooks/update_dynamic_content.py` - MkDocs pre-build hook
- `docs/README.md` - Documentation maintenance guide
- `bin/validate_docs.py` - Documentation validator
- `docs/reference/parameters.md` - Auto-generated parameter documentation
- `DOCUMENTATION_UPDATES.md` - This file

## Automation Features

### Before Each Build
1. ✅ Parameter documentation regenerated from schema
2. ✅ Version extracted from nextflow.config
3. ✅ Version placeholders replaced in markdown

### Manual Commands
```bash
# Regenerate parameter docs
python3 bin/generate_parameter_docs.py

# Validate all documentation
python3 bin/validate_docs.py

# Preview locally
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Verification

All changes have been validated:

- ✅ Mermaid diagrams syntax validated
- ✅ Internal links checked
- ✅ Parameter documentation generated successfully
- ✅ Hook integration tested
- ✅ Color scheme applied consistently
- ✅ Broken links fixed

## Future Maintenance

To keep documentation updated:

1. **When adding parameters**: Update `nextflow_schema.json`, docs auto-update
2. **When modifying workflow**: Update mermaid diagrams in relevant files
3. **When adding processes**: Update process table in `docs/architecture/design.md`
4. **Before releases**: Run `python3 bin/validate_docs.py`

## Benefits

1. **Accuracy**: Documentation now matches actual pipeline implementation
2. **Automation**: Parameter docs always reflect current schema
3. **Maintainability**: Clear guidelines and validation tools
4. **Visual Clarity**: Consistent color scheme and improved diagrams
5. **Completeness**: All pipeline paths and dependencies documented

## Notes

- Analysis modules (IPSAE, PRODIGY, Foldseek) **require both** `--run_proteinmpnn` and `--run_boltz2_refold`
- These modules **only process Boltz-2 structures**, not original Boltzgen designs
- Precomputed Boltzgen results can be reused via `boltzgen_output_dir` in samplesheet
- All GPU-accelerated processes are clearly marked in diagrams

---

**Validation Status**: ✅ All checks passed  
**Build Status**: ✅ Ready for deployment  
**Generated**: 2025-12-02

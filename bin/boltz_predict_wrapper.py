#!/usr/bin/env python3
"""
Wrapper for boltz predict that sets torch.set_float32_matmul_precision
before running predictions, enabling optimal Tensor Core utilization on
NVIDIA GPUs like A100 and H100.

Usage:
    boltz_predict_wrapper.py [--precision medium|high] -- <boltz predict args...>

Example:
    boltz_predict_wrapper.py --precision medium -- input.yaml --out_dir results
"""

import argparse
import os
import sys


def main():
    # Parse wrapper-specific args
    parser = argparse.ArgumentParser(
        description="Wrapper for boltz predict with torch precision settings",
        add_help=False
    )
    parser.add_argument(
        "--precision",
        choices=["medium", "high", "highest"],
        default="medium",
        help="Float32 matmul precision level (default: medium)"
    )

    # Find the -- separator
    if "--" in sys.argv:
        sep_idx = sys.argv.index("--")
        wrapper_args = sys.argv[1:sep_idx]
        boltz_args = sys.argv[sep_idx + 1:]
    else:
        # No separator, assume all args are for boltz
        wrapper_args = []
        boltz_args = sys.argv[1:]

    args, _ = parser.parse_known_args(wrapper_args)

    # Set precision BEFORE importing torch (boltz imports torch)
    os.environ["TORCH_FLOAT32_MATMUL_PRECISION"] = args.precision

    # Now import torch and set precision programmatically
    import torch
    torch.set_float32_matmul_precision(args.precision)
    print(f"Set torch.set_float32_matmul_precision('{args.precision}')", file=sys.stderr)

    # Import boltz CLI and run
    from boltz.main import cli

    # Construct the full command for boltz
    # cli expects: boltz predict <args>
    sys.argv = ["boltz", "predict"] + boltz_args

    cli()


if __name__ == "__main__":
    main()

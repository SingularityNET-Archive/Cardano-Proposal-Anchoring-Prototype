#!/usr/bin/env python3
"""Wrapper script for backwards compatibility."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from commands.anchor_proposal import main  # pyright: ignore[reportMissingImports]

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compatibility entry point for the current four-source validation."""
import importlib.util
from pathlib import Path
path = Path(__file__).with_name('validate-current.py')
spec = importlib.util.spec_from_file_location('current_validation', path)
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)
if __name__ == '__main__':
    validation.validate()

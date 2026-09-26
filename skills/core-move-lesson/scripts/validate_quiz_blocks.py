#!/usr/bin/env python3
"""Compatibility entry point for the canonical quiz-block-factory validator."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


FACTORY_VALIDATOR = (
    Path(__file__).resolve().parents[2]
    / "quiz-block-factory"
    / "scripts"
    / "validate_quiz_blocks.py"
)

_spec = importlib.util.spec_from_file_location("quiz_block_factory_validator", FACTORY_VALIDATOR)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Could not load quiz-block validator: {FACTORY_VALIDATOR}")
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)

Issue = _module.Issue
QuizBlock = _module.QuizBlock
extract_quiz_blocks = _module.extract_quiz_blocks
validate_block = _module.validate_block
validate_file = _module.validate_file
main = _module.main


if __name__ == "__main__":
    raise SystemExit(main())

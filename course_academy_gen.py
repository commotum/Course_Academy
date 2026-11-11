"""Repository-local entry point for ``uv run gen``."""
from pathlib import Path
import sys


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent / 'scripts'))
    from gen_cli import main as run
    return run()

"""Supports both `python capture/scripts` and package execution."""
if not __package__:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from scripts.cli import main
else:
    from .cli import main

raise SystemExit(main())

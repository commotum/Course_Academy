"""Materialize independent review controls in a temporary directory."""
import argparse
import json
from pathlib import Path
import shutil
import sys


CASES = {"a": "selected_entry", "b": "fixed_entry", "c": "diagonal_sum"}


def build(destination):
    destination = Path(destination)
    origin = Path(__file__).resolve().parent
    source = destination / "source"
    source.mkdir(parents=True, exist_ok=True)
    for name in ("source.md", "source-cases.json"):
        shutil.copyfile(origin / name, source / name)
    for name, sampling in CASES.items():
        package = destination / name
        package.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin / "generator.py", package / "generator.py")
        (package / "behavior.json").write_text(json.dumps({"sampling": sampling}) + "\n")
        (package / "package.json").write_text(json.dumps({
            "entrypoint": "generator.py", "files": ["generator.py", "behavior.json"],
            "dependencies": {"python": sys.version.split()[0], "packages": {}},
        }, indent=2) + "\n")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    print(build(parser.parse_args().destination))

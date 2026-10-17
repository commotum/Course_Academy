#!/usr/bin/env python3
"""Rebuild the grader/app atomically without restarting the app or accessing EDB."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("grader", "app", "both"), required=True)
    args = parser.parse_args()
    report = {
        "target": args.target, "database_operations": 0, "app_restarted": False,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "learning_source_sha256": sha256(ROOT / "engine/rust/learning.rs"),
        "rustc": subprocess.check_output(["rustc", "--version"], text=True).strip(),
        "cargo": subprocess.check_output(["cargo", "--version"], text=True).strip(),
    }
    if args.target in ("app", "both"):
        sys.path.insert(0, str(ROOT / "scripts"))
        from serve_graph_explorer import build_learning

        # This compiles a new versioned executable and atomically renames it.
        # The running app continues using its existing executable until restarted.
        app = build_learning(ROOT.parent / "EDB")
        report["app"] = {"path": str(app), "sha256": sha256(app)}
    else:
        subprocess.run(
            ["cargo", "build", "--release", "--lib", "--offline"], cwd=ROOT, check=True
        )
    if args.target in ("grader", "both"):
        deps = ROOT / "target/release/deps"
        output = ROOT / "generate/runs/current/check-engine"
        staging = output.with_name(f"{output.name}.tmp-{os.getpid()}")
        command = [
            "rustc", "--edition=2024", "-O",
            str(ROOT / "generate/runs/current/check-engine.rs"),
        ]
        libraries = {}
        for name in ("course_academy_engine", "serde_json"):
            library = max(deps.glob(f"lib{name}-*.rlib"), key=lambda p: p.stat().st_mtime_ns)
            libraries[name] = {"path": str(library), "sha256": sha256(library)}
            command.extend(["--extern", f"{name}={library}"])
        command.extend(["-L", f"dependency={deps}", "-o", str(staging)])
        previous = sha256(output) if output.exists() else None
        try:
            subprocess.run(command, cwd=ROOT, check=True)
            # Exercise the actual grade_field entry point before replacement.
            subprocess.run(
                [str(staging), str(EVIDENCE / "fraction-form-native-input.json"),
                 str(EVIDENCE / "fraction-form-native-result.json")],
                cwd=ROOT, check=True,
            )
            staging.replace(output)
        finally:
            staging.unlink(missing_ok=True)
        report["grader"] = {
            "path": str(output), "previous_sha256": previous, "sha256": sha256(output),
            "source_sha256": sha256(ROOT / "generate/runs/current/check-engine.rs"),
            "libraries": libraries, "command": command,
            "smoke_input_sha256": sha256(EVIDENCE / "fraction-form-native-input.json"),
            "smoke_result_sha256": sha256(EVIDENCE / "fraction-form-native-result.json"),
        }
    report["completed_at"] = datetime.now(timezone.utc).isoformat()
    path = EVIDENCE / f"fraction-form-rebuild-{args.target}.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

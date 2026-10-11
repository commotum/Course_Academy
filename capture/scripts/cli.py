"""Run the replacement, inspect without submitting, or process saved captures."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import json
import logging
from pathlib import Path
import shlex
import sys
import threading

from .config import Config
from .outbox import DatabaseWorker
from .runtime import StopRequested, shutdown_signals
from .storage import file_lock, read_json


def parser():
    cli = argparse.ArgumentParser(description="Resumable Math Academy content capture")
    cli.add_argument("command", choices=["run", "fleet", "inspect", "status", "prepare", "drain", "check"])
    cli.add_argument("capture_directory", nargs="?", type=Path, help="Completed capture for prepare")
    cli.add_argument("--config", type=Path, help="JSON configuration file")
    cli.add_argument("--account", help="Account name: foundations, linear, multivariable, or differential")
    cli.add_argument("--repo-root", type=Path)
    cli.add_argument("--state-root", type=Path)
    cli.add_argument("--output-root", type=Path)
    cli.add_argument("--profile", type=Path)
    cli.add_argument("--course-id")
    cli.add_argument("--target", action="append", dest="targets", help="Downstream target topic ID; repeat for multiple targets")
    cli.add_argument("--learner-id", help="Learner identity whose study and assignment targets determine priority")
    cli.add_argument("--math-root", type=Path)
    cli.add_argument("--edb-bin", type=Path)
    cli.add_argument("--endpoint")
    cli.add_argument("--database")
    cli.add_argument("--postgres-url")
    cli.add_argument("--derived-source", help="Existing source ident for calculated difficulty; otherwise save it locally")
    cli.add_argument("--visible", action="store_true", default=None)
    cli.add_argument("--capture-only", action="store_true", default=None, help="Perform MA activities and retain evidence without database writes")
    cli.add_argument("--solver-command", help="External JSON solver command; parsed without a shell")
    cli.add_argument("--codex-bin")
    cli.add_argument("--solver-model")
    cli.add_argument("--solver-timeout", type=float)
    cli.add_argument("--seed", type=int)
    cli.add_argument("--once", action="store_true", help="For drain: process the oldest pending capture once")
    return cli


def configuration(args):
    values = vars(args).copy()
    for key in ("command", "capture_directory", "once", "config"):
        values.pop(key)
    visible = values.pop("visible")
    if visible is not None:
        values["headless"] = not visible
    if values.get("solver_command"):
        values["solver_command"] = shlex.split(values["solver_command"])
    return Config.from_file(args.config, **values)


def main(argv=None):
    args = parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if args.command == "fleet":
        from .fleet import run_fleet
        return run_fleet(list(argv if argv is not None else sys.argv[1:]))
    config = configuration(args)
    stop = threading.Event()
    if args.command == "status":
        value = {"account": config.account, "capture": read_json(config.state_root / "status.json", {}),
            "active": read_json(config.state_root / "active.json"),
            "pending_imports": len(DatabaseWorker(config, stop, None).pending())}
        print(json.dumps(value, indent=2))
        return 0
    if args.command == "check":
        import importlib.util
        value = {"account": config.account, "course_id": config.course_id,
            "profile_exists": config.profile.is_dir(), "edb_binary_exists": config.edb_bin.is_file(),
            "dependencies": {name: importlib.util.find_spec(name) is not None for name in ("playwright", "bs4", "PIL")},
            "output_root": str(config.output_root), "state_root": str(config.state_root),
            "math_root": str(config.math_root), "capture_only": config.capture_only}
        print(json.dumps(value, indent=2))
        return 0 if all(value["dependencies"].values()) and value["profile_exists"] else 1
    with shutdown_signals(stop):
        try:
            if args.command == "run":
                from .runner import CaptureRunner
                CaptureRunner(config, stop).run()
            elif args.command == "inspect":
                from .browser import MathAcademyBrowser
                from .queue_processing import read_queue
                from .selection import choose
                from .database import DatabasePipeline
                from .context import ContextProvider
                with ExitStack() as stack:
                    for lock in sorted({config.state_root / "capture.lock", config.profile.parent / "capture.lock"}, key=str):
                        stack.enter_context(file_lock(lock, blocking=False))
                    browser = stack.enter_context(MathAcademyBrowser(config, stop))
                    queue = read_queue(browser, config.state_root / "queue")
                    context = ContextProvider(config, lambda: DatabasePipeline(config, stop))({"course_id": config.course_id})
                    print(json.dumps({"activities": queue, "selected": choose(queue, context)}, indent=2))
            elif args.command == "prepare":
                if args.capture_directory is None:
                    parser().error("prepare requires a completed capture directory")
                from .database import DatabasePipeline
                with file_lock(config.database_lock):
                    result = DatabasePipeline(config, stop).process(args.capture_directory, apply=False)
                print(json.dumps(result, indent=2))
            elif args.command == "drain":
                from .database import DatabasePipeline
                worker = DatabaseWorker(config, stop, lambda: DatabasePipeline(config, stop))
                if args.once:
                    print(json.dumps(worker.process_one(), indent=2))
                else:
                    worker.run()
        except (StopRequested, KeyboardInterrupt):
            stop.set()
        finally:
            stop.set()
    return 0

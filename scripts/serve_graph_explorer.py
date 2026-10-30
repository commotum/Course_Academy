#!/usr/bin/env python3
"""Serve the graph explorer and durable learner app on http://127.0.0.1:8765.

Run: python3 scripts/serve_graph_explorer.py
Uses the math database at /media/jake/SSD/EDB/math and its edb_peer role
unless EDB_POSTGRES_URL is supplied.
The native reader is built against EDB_ROOT (defaults to the adjacent EDB repo)
and existing serde_json build artifacts from this repository or EDB_ROOT.
The learner helper uses the release engine and the existing local EDB writer.
Open /home for the queue and /learn?taskId=... for a saved lesson attempt.
Open /progress?course=... for a course outline and the learner's topic progress.
Open /topic?topic=... for tutorials and worked examples without starting a lesson.
Open /assignments for schoolwork and /assignments?assignment=... for its problems.
"""

from __future__ import annotations

import argparse
from contextlib import nullcontext
import fcntl
import functools
import gzip
import hashlib
import json
import mimetypes
import os
import select
import signal
from pathlib import Path
import subprocess
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from inventory_jobs import InventoryJobs, build_worker_count, review_worker_count
from study_outbox_compat import CompatibleStudyOutbox
from read_cache import ReadCache
from graph_preferences import read_preferences, update_preferences

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ui" / "Math-Academy-Graph-Explorer.html"
SOURCE = ROOT / "scripts" / "graph_explorer_reader.rs"
DEFAULT_LEARNER = "59d5cf13-351c-4114-be19-4c3bb64ee051"
DEFAULT_DATABASE = "math"
DEFAULT_MATH_ROOT = Path("/media/jake/SSD/EDB/math")
DEFAULT_POSTGRES_URL = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"
DEFAULT_ENDPOINT = "/tmp/edb-math/writer.sock"
ASSET_ROOTS = (ROOT.parent / "MA/DATA/Lessons", ROOT.parent / "study/vault",
               ROOT / "reference/mathacademy/history-question-import-2026-10-04/import-ready/assets")
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}
MUTATING_ACTIONS = {"draft", "navigate", "submit", "start", "study-topic", "review-topic", "answer", "skip", "expire", "continue", "pause", "resume", "target", "queue", "queue-topic",
                    "assignment-focus", "assignment-answer", "assignment-pause", "regenerate-assessment"}
# These handlers only inspect captured state. Neither writer admission nor an
# unrelated transaction may hold their HTTP responses behind api.lock.
READ_ACTIONS = {"home", "profile", "learner", "task", "assignment", "assignments",
                "activity-history", "activity-history-detail", "study-stats",
                "forecast-inputs", "topic-study-availability", "inventory",
                "preview-home", "preview", "preview-answer", "preview-active-tasks"}
CACHED_READ_ACTIONS = {"assignments", "activity-history", "activity-history-detail",
                       "study-stats", "forecast-inputs", "home", "preview-home"}


def database_environment(database: str) -> dict[str, str]:
    environment = os.environ.copy()
    environment.setdefault("EDB_POSTGRES_URL", DEFAULT_POSTGRES_URL)
    environment.setdefault("EDB_CONNECT_TIMEOUT_MS", "5000")
    environment.setdefault("EDB_STATEMENT_TIMEOUT_MS", "15000")
    environment.setdefault("EDB_ENDPOINT", DEFAULT_ENDPOINT)
    environment.setdefault("EDB_MATH_ROOT", str(DEFAULT_MATH_ROOT))
    environment.setdefault("LEARNING_REQUEST_DIR", str(ROOT / ".local/learning/requests" / database))
    return environment


def image_path(value: str, math_root: Path) -> Path | None:
    """Resolve database-relative images without exposing other database files."""
    if not value:
        return None
    asset = Path(value)
    if not asset.is_absolute():
        if not asset.parts or asset.parts[0] != "images":
            return None
        asset = math_root / asset
    try:
        asset = asset.resolve()
        roots = (*ASSET_ROOTS, math_root / "images")
        if asset.suffix.lower() in IMAGE_TYPES and any(asset.is_relative_to(root.resolve()) for root in roots) and asset.is_file():
            return asset
    except (OSError, RuntimeError, ValueError):
        pass
    return None


def developer_mode(path: Path) -> bool:
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError:
        return False
    if not isinstance(value, dict) or type(value.get("enabled")) is not bool:
        raise ValueError("Invalid developer mode setting; recording remains blocked")
    return value["enabled"]


def save_developer_mode(path: Path, enabled: bool) -> None:
    save_json(path, {"enabled": enabled})


def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_suffix(".tmp")
    with staging.open("w") as stream:
        json.dump(value, stream)
        stream.flush()
        os.fsync(stream.fileno())
    staging.replace(path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def focused_mode_path(directory: Path, learner: str) -> Path:
    return directory / f"{learner}-focused-mode.json"


def focused_mode(path: Path) -> bool | None:
    """An absent profile preference retains the code's existing default."""
    try:
        value = json.loads(path.read_text())
    except FileNotFoundError:
        return None
    if not isinstance(value, dict) or type(value.get('enabled')) is not bool:
        raise ValueError('Invalid focused-mode preference')
    return value['enabled']


def assignment_request(body: dict, directory: Path, learner: str) -> dict:
    """Under api.lock, let an unload pause cancel a focus that arrives later."""
    action = body.get("action")
    request = body.get("cancelFocusRequestId") if action == "assignment-pause" else body.get("requestId")
    if action not in {"assignment-focus", "assignment-pause"} or request is None:
        return body
    if not isinstance(request, str) or not 8 <= len(request) <= 100 or not all(c.isascii() and (c.isalnum() or c == "-") for c in request):
        raise ValueError("Invalid assignment focus request ID")
    key = hashlib.sha256(json.dumps([learner, request]).encode()).hexdigest()
    marker = directory / f"assignment-focus-cancel-{key}.json"
    if action == "assignment-pause":
        assignment = body.get("assignmentId")
        if not isinstance(assignment, str) or not assignment:
            raise ValueError("Canceling a focus requires its assignment ID")
        save_json(marker, {"assignmentId": assignment})
    elif marker.exists():
        canceled = json.loads(marker.read_text())
        if not isinstance(canceled, dict) or canceled.get("assignmentId") != body.get("assignmentId"):
            raise ValueError("Canceled focus assignment does not match")
        return {"action": "assignment", "assignmentId": body["assignmentId"], "preview": False}
    return body


def admit_answer(body: dict, directory: Path, learner: str, received: int) -> dict:
    """Keep the first server-observed submission time across retries and conflicts."""
    if body.get('action') != 'answer':
        return body
    request = body.get('requestId', '')
    if isinstance(request, str) and 8 <= len(request) <= 128 and all(c.isascii() and (c.isalnum() or c == '-') for c in request):
        journal = directory / f'{learner}-{request}.json'
        if journal.exists():
            saved_input = json.loads(journal.read_text()).get('input')
            if saved_input == body:
                # Existing receipts retain their exact input across deployment.
                return body
    key = body.get('submissionId', body.get('requestId', ''))
    if not isinstance(key, str) or not 8 <= len(key) <= 128 or not all(c.isascii() and (c.isalnum() or c == '-') for c in key):
        raise ValueError('A stable submission ID is required')
    original = {k: v for k, v in body.items() if k not in {'requestId', 'submittedAt'}}
    folder = directory / 'admissions'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f'{learner}-{key}.json'
    with (folder / 'admission.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if path.exists():
            saved = json.loads(path.read_text())
            if saved['input'] != original:
                raise ValueError('Submission ID already used for a different answer')
        else:
            saved = {'input': original, 'submittedAt': received}
            staging = path.with_suffix('.tmp')
            with staging.open('w') as output:
                json.dump(saved, output, separators=(',', ':'))
                output.flush()
                os.fsync(output.fileno())
            staging.replace(path)
            descriptor = os.open(folder, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    return {**body, 'submittedAt': saved['submittedAt']}


class NativeWorker:
    """Keep EDB's connection and immutable block caches resident between requests."""

    def __init__(self, command: list[str], environment: dict[str, str], name: str):
        self.command, self.environment = command, environment
        self.log_path = ROOT / ".local/graph-explorer" / f"{name}.log"
        self.process = None
        self.lock = threading.Lock()

    def _stop(self):
        process, self.process = self.process, None
        if process is None:
            return
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        for pipe in (process.stdin, process.stdout):
            pipe.close()

    def close(self):
        with self.lock:
            self._stop()

    def request(self, body: dict, timeout: float = 55) -> dict:
        with self.lock:
            try:
                # Only the server's saved preference can set this internal policy.
                # It is removed by the native boundary before durable journaling.
                if len(self.command) >= 5 and 'LEARNING_REQUEST_DIR' in self.environment:
                    body = {k: v for k, v in body.items() if k != '_focusedMode'}
                    preference = focused_mode(focused_mode_path(
                        Path(self.environment['LEARNING_REQUEST_DIR']), self.command[2]))
                    if preference is not None:
                        body['_focusedMode'] = preference
                if self.process is None or self.process.poll() is not None:
                    self._stop()
                    self.log_path.parent.mkdir(parents=True, exist_ok=True)
                    with self.log_path.open("ab") as log:
                        self.process = subprocess.Popen(self.command, env=self.environment,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, bufsize=0)
                process = self.process
                data = json.dumps(body, separators=(",", ":")).encode() + b"\n"
                pending = memoryview(data)
                while pending:
                    written = process.stdin.write(pending)
                    if not written:
                        raise OSError("Native database worker input closed")
                    pending = pending[written:]
                process.stdin.flush()
                deadline, output = time.monotonic() + timeout, bytearray()
                while True:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0 or not select.select([process.stdout], [], [], remaining)[0]:
                        raise TimeoutError("Native database request timed out")
                    chunk = os.read(process.stdout.fileno(), 65536)
                    if not chunk:
                        raise OSError("Native database worker stopped")
                    output.extend(chunk)
                    if len(output) > 32 * 1024 * 1024:
                        raise ValueError("Native response exceeds limit")
                    if b"\n" in chunk:
                        response = json.loads(output)
                        if not isinstance(response, dict):
                            raise ValueError("Invalid native response")
                        return response
            except (OSError, ValueError):
                # Never silently replay a write with an uncertain outcome. The caller
                # retains its request ID; the native durable journal handles retries.
                self._stop()
                raise


@functools.lru_cache(maxsize=16)
def compressed(body: bytes) -> bytes:
    return gzip.compress(body, compresslevel=5, mtime=0)


def build_learning(edb_root: Path, *, test: bool = False) -> Path:
    subprocess.run(["cargo", "build", "--release", "--lib", "--offline"], cwd=ROOT, check=True)
    source = ROOT / "scripts/learning_api.rs"
    edb_deps = edb_root / "target/release/deps"
    deps = ROOT / "target/release/deps"
    libraries = {}
    for name, directory in (("edb_core", edb_deps), ("serde_json", deps), ("chrono", deps), ("course_academy_engine", deps)):
        libraries[name] = max(directory.glob(f"lib{name}-*.rlib"), key=lambda p: p.stat().st_mtime_ns)
    sources = (source, ROOT / "scripts/review_interaction.rs", ROOT / "scripts/study_interaction.rs", ROOT / "scripts/page_reader.rs", ROOT / "scripts/activity_history.rs", ROOT / "scripts/assignment_reader.rs", ROOT / "scripts/assignment_interaction.rs",
               ROOT / "scripts/developer_preview.rs", ROOT / "scripts/study_stats.rs", ROOT / "scripts/forecast_reader.rs", ROOT / "scripts/quiz_labels.rs")
    if test:
        sources += (ROOT / "scripts/assignment_interaction_tests.rs", ROOT / "scripts/retrieval_tests.rs",
                    ROOT / "engine/edb/progress.rs", ROOT / "engine/edb/configuration.rs",
                    ROOT / "engine/edb/answer_fields.rs")
    fingerprint = hashlib.sha256(b"".join(p.read_bytes() for p in sources) + repr((test, [(str(p), p.stat().st_mtime_ns) for p in libraries.values()])).encode()).hexdigest()[:16]
    output = ROOT / ".local/graph-explorer" / f"learning-{fingerprint}"
    if not output.exists():
        output.parent.mkdir(parents=True, exist_ok=True)
        staging = output.with_suffix(f".tmp-{os.getpid()}")
        command = ["rustc", "--edition=2024", "-O", str(source)]
        if test:
            command.append("--test")
        for name, path in libraries.items():
            command.extend(["--extern", f"{name}={path}"])
        command.extend(["-L", f"dependency={edb_deps}", "-L", f"dependency={deps}", "-o", str(staging)])
        try:
            subprocess.run(command, check=True)
            staging.replace(output)
        finally:
            staging.unlink(missing_ok=True)
    return output


def build_reader(edb_root: Path, *, test: bool = False) -> Path:
    edb_deps = edb_root / "target" / "release" / "deps"
    libraries = sorted(edb_deps.glob("libedb_core-*.rlib"))
    if len(libraries) != 1:
        raise RuntimeError(f"Expected one release edb_core library in {edb_deps}; build EDB first.")
    serde = None
    for directory in (ROOT / "target/debug/deps", ROOT / "target/release/deps", edb_deps, edb_root / "target/debug/deps"):
        candidates = list(directory.glob("libserde_json-*.rlib"))
        if candidates:
            serde = max(candidates, key=lambda path: path.stat().st_mtime_ns)
            break
    if serde is None:
        raise RuntimeError("Missing serde_json build artifact; run `cargo build --lib --offline` in this repository first.")
    sources = (SOURCE, ROOT / "scripts/topic_reader.rs", ROOT / "engine/rust/study_mode.rs")
    inputs = (*sources, libraries[0], serde)
    fingerprint = hashlib.sha256(str(test).encode() + b"optimized-reader-v1" + b"".join(path.read_bytes() for path in sources) + repr([
        (str(path), path.stat().st_size, path.stat().st_mtime_ns) for path in inputs
    ]).encode()).hexdigest()[:16]
    output = ROOT / ".local" / "graph-explorer" / f"reader-{fingerprint}"
    if not output.exists():
        output.parent.mkdir(parents=True, exist_ok=True)
        staging = output.with_suffix(f".tmp-{os.getpid()}")
        try:
            subprocess.run([
                "rustc", "--edition=2024", "-O", str(SOURCE),
                *(["--test"] if test else []),
                "--extern", f"edb_core={libraries[0]}", "--extern", f"serde_json={serde}",
                "-L", f"dependency={edb_deps}", "-L", f"dependency={serde.parent}",
                "-o", str(staging),
            ], check=True)
            staging.replace(output)
        finally:
            staging.unlink(missing_ok=True)
    return output


def handler(reader: Path, database: str, learner: str, environment: dict[str, str], learning: Path | None = None):
    public_origin = environment.get("COURSE_ACADEMY_PUBLIC_ORIGIN", "").strip()
    public_host = None
    if public_origin:
        parsed = urlsplit(public_origin)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
                or parsed.password is not None or parsed.path not in ("", "/")
                or parsed.query or parsed.fragment or parsed.port == 0):
            raise ValueError("COURSE_ACADEMY_PUBLIC_ORIGIN must be an HTTPS origin without a path")
        public_host = parsed.netloc.lower()
        public_origin = f"https://{public_host}"
    graph_worker = NativeWorker([str(reader), database, learner, "--serve"], environment, "graph-worker")
    learning_worker = NativeWorker([str(learning), database, learner, environment["EDB_ENDPOINT"], "--serve"], environment, "learning-worker") if learning else None
    page_worker = NativeWorker([str(learning), database, learner, "--pages", "--serve"], environment, "page-worker") if learning else None
    stats_worker = NativeWorker([str(learning), database, learner, "--pages", "--serve"], environment, "stats-worker") if learning else None
    scheduler_worker = NativeWorker([str(learning), database, learner, environment["EDB_ENDPOINT"], "--serve"], environment, "scheduler-worker") if learning else None
    feedback_worker = NativeWorker([str(learning), database, learner, environment["EDB_ENDPOINT"], "--serve"], environment, "feedback-worker") if learning else None
    persistence_worker = NativeWorker([str(learning), database, learner, environment["EDB_ENDPOINT"], "--serve"], environment, "review-save-worker") if learning else None
    read_worker = NativeWorker([str(learning), database, learner, environment["EDB_ENDPOINT"], "--serve"], environment, "study-read-worker") if learning else None
    forecast_worker = NativeWorker([str(learning), database, learner, "--pages", "--serve"], environment, "forecast-read-worker") if learning else None
    read_cache = ReadCache()
    request_directory = Path(environment["LEARNING_REQUEST_DIR"])
    graph_preferences_path = Path(environment.get('COURSE_ACADEMY_GRAPH_PREFERENCES', ROOT / '.local/graph-preferences.json'))
    mode_path = request_directory / "developer-mode.json"
    math_root = Path(environment.get("EDB_MATH_ROOT", DEFAULT_MATH_ROOT)).resolve()

    inventory_jobs = InventoryJobs(ROOT, ROOT / '.local/learning/inventory' / database / learner, learner, environment)
    builder_count = build_worker_count(environment)
    review_worker_count(environment, builder_count)
    scheduler_stop = threading.Event()
    inventory_refresh = threading.Event()
    inventory_ready = threading.Event()
    inventory_refresh.set()
    def progress_saved():
        read_cache.invalidate()
        inventory_refresh.set()
    review_outbox = CompatibleStudyOutbox(request_directory / "review-outbox", feedback_worker, persistence_worker, save_json, scheduler_stop, progress_saved) if learning_worker else None
    candidate_reader = None

    def inventory_hook():
        nonlocal candidate_reader
        # The finder owns its read connection. Never put its catalog scan under
        # api.lock or on the learning worker used to answer learner requests.
        if str(ROOT / 'generate/scripts') not in sys.path:
            sys.path.insert(0, str(ROOT / 'generate/scripts'))
        from find_candidates import build, discover
        if candidate_reader is None:
            candidate_reader = build(Path(environment.get('EDB_ROOT', ROOT.parent / 'EDB')).resolve())
        ranked = discover(database, learner, environment, binary=candidate_reader, include_registered=True)
        inventory_jobs.accept(ranked)
        if not inventory_ready.is_set():
            print(f"Ranked generator inventory ready: basis {ranked['basis']}, "
                  f"{len(ranked['knowledge_points'])} build candidates", flush=True)
        inventory_ready.set()

    def scheduler_loop():
        # NativeWorker incrementally consumes the EDB log into one held projection;
        # scans also cover age/retention transitions without a new transaction.
        while not scheduler_stop.is_set():
            try:
                request_directory.mkdir(parents=True, exist_ok=True)
                with (request_directory / 'api.lock').open('a') as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    if not developer_mode(mode_path):
                        response = scheduler_worker.request({'action': 'queue', 'background': True, 'requestId': 'scheduler-' + os.urandom(12).hex()})
                        if not response.get('ok'):
                            raise ValueError(response.get('error', 'Queue preparation unavailable'))
                        inventory_refresh.set()
            except (OSError, ValueError) as error:
                print(f'Scheduler refresh deferred: {error}', file=sys.stderr)
            scheduler_stop.wait(30)

    def run_generator_lane(lane, slot=0):
        while not scheduler_stop.is_set():
            try:
                if (inventory_ready.is_set() and not developer_mode(mode_path)
                        and environment.get('COURSE_ACADEMY_DISABLE_GENERATION') != '1'):
                    if inventory_jobs.run_one(lane=lane, slot=slot):
                        inventory_refresh.set()
            except Exception as error:
                # A bad job or unexpected runtime error must not permanently
                # remove a worker lane while the HTTP service still looks live.
                # Job retry budgets remain in run_one; this supervisor retains
                # the lane and waits before its next admission attempt.
                print(f'Inventory {lane} worker {slot + 1} deferred: {error}', file=sys.stderr)
                traceback.print_exc()
            scheduler_stop.wait(5)

    def build_loop(slot):
        def generator_build_loop():
            run_generator_lane('build', slot)
        generator_build_loop.worker_slot = slot
        return generator_build_loop

    def generator_refill_loop():
        run_generator_lane('refill')

    def inventory_refresh_loop():
        # Inventory admission is read-only background work, not part of the
        # response to a saved lesson. Coalesce requests while a scan is running.
        while not scheduler_stop.is_set():
            if not inventory_refresh.wait(1):
                continue
            try:
                inventory_refresh.clear()
                if not developer_mode(mode_path):
                    inventory_hook()
            except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
                print(f'Inventory handoff deferred: {error}', file=sys.stderr)
                inventory_refresh.set()
                scheduler_stop.wait(5)

    class Handler(BaseHTTPRequestHandler):
        def send_bytes(self, status: int, body: bytes, content_type: str, *, cache: bool = False) -> None:
            etag = 'W/"' + hashlib.sha256(body).hexdigest() + '"' if cache else None
            validators = {v.strip().removeprefix("W/") for v in self.headers.get("If-None-Match", "").split(",")}
            not_modified = cache and ("*" in validators or etag.removeprefix("W/") in validators)
            compressible = content_type.startswith(("text/", "application/json", "image/svg+xml"))
            accepts_gzip = any(part.strip().split(";", 1)[0] == "gzip" and not any(q.strip() in {"q=0", "q=0.0", "q=0.00", "q=0.000"} for q in part.split(";")[1:]) for part in self.headers.get("Accept-Encoding", "").split(","))
            zipped = not not_modified and accepts_gzip and compressible and 1024 <= len(body) <= 4 * 1024 * 1024
            if zipped:
                body = compressed(body)
            if not_modified:
                status = 304
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            if not not_modified:
                self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "private, no-cache" if cache else "no-store")
            self.send_header("Vary", "Accept-Encoding")
            if etag:
                self.send_header("ETag", etag)
            if zipped:
                self.send_header("Content-Encoding", "gzip")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "same-origin")
            if content_type == "image/svg+xml":
                self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; sandbox")
            self.end_headers()
            if self.command != "HEAD" and not not_modified:
                self.wfile.write(body)

        def trusted(self) -> bool:
            host = self.headers.get("Host", "").lower()
            allowed_origins = {f"{name}:{self.server.server_port}": f"http://{name}:{self.server.server_port}"
                               for name in ("127.0.0.1", "localhost")}
            if public_host:
                allowed_origins[public_host] = public_origin
            origin = self.headers.get("Origin")
            if host not in allowed_origins or (origin and origin != allowed_origins[host]):
                self.send_bytes(403, b"Forbidden", "text/plain; charset=utf-8")
                return False
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                self.send_bytes(403, b"Forbidden", "text/plain; charset=utf-8")
                return False
            return True

        def learning_request(self, body: dict) -> None:
            request_started = time.monotonic()
            received = time.time_ns() // 1_000_000
            if learning_worker is None:
                self.send_bytes(503, b'{"error":"Learning API is unavailable."}', "application/json")
                return
            try:
                directory = Path(environment["LEARNING_REQUEST_DIR"])
                directory.mkdir(parents=True, exist_ok=True)
                body = admit_answer(body, directory, learner, received)
                # Never accept server-only command envelopes from HTTP callers.
                if any(key.startswith('_') for key in body):
                    raise ValueError("Private interaction fields are not accepted")
                if review_outbox and not developer_mode(mode_path):
                    action = body.get('action')
                    if action in {'review-save-status', 'review-save-retry'}:
                        value = (review_outbox.retry if action == 'review-save-retry' else review_outbox.status)(body['taskId'])
                        self.send_bytes(200, json.dumps(value).encode(), "application/json")
                        return
                    value = review_outbox.overlay_view(action, body)
                    if value is not None:
                        self.send_bytes(200, json.dumps(value).encode(), "application/json")
                        return
                    value = review_outbox.request(body, received)
                    if value is not None:
                        if '_error' in value:
                            self.send_bytes(409, json.dumps({'error': value['_error'], 'code': value['_code']}).encode(), "application/json")
                        else:
                            read_cache.invalidate()
                            self.send_bytes(200, json.dumps(value).encode(), "application/json")
                        print(f"Learning immediate {action}: {(time.monotonic()-request_started)*1000:.1f} ms", file=sys.stderr)
                        return
                    body = review_outbox.resolve_ids(body)

                # Shared across request threads and server processes. Native writes also
                # compare the EDB basis, covering writers outside this application.
                page_read = body.get("action") in {"assignments", "activity-history", "study-stats", "forecast-inputs"}
                # Immutable list reads have their own peer and never record
                # learner state. Scheduler/write admission must not block them.
                # Publishers can spend minutes validating under api.lock. Answers
                # use the held native peer's mutex plus EDB's exact basis/status
                # guards, so they may proceed while content is being prepared.
                with (nullcontext() if body.get('action') in READ_ACTIONS | {'answer'} else (directory / "api.lock").open("a")) as lock:
                    if lock is not None:
                        fcntl.flock(lock, fcntl.LOCK_EX)
                    admitted = time.monotonic()
                    if body.get("action") in MUTATING_ACTIONS and developer_mode(mode_path):
                        self.send_bytes(409, b'{"error":"Developer mode is on. No activity or learner changes are recorded.","code":"developer-mode"}', "application/json")
                        return
                    focus_change = body.get('action') == 'focused-mode'
                    if focus_change:
                        if type(body.get('focusedMode')) is not bool:
                            raise ValueError('Focused mode must be a boolean')
                        save_json(focused_mode_path(directory, learner), {'enabled': body['focusedMode']})
                        body = {'action': 'profile'}
                    if body.get("action") == "assignment":
                        # The server setting selects inspection-only answer keys;
                        # a request cannot promote itself into developer mode.
                        body = {**body, "preview": developer_mode(mode_path)}
                    body = assignment_request(body, directory, learner)
                    # XP must not wait behind a forecast or activity-history read.
                    action = body.get('action')
                    worker = (stats_worker if action == 'study-stats' else
                              forecast_worker if action == 'forecast-inputs' else
                              page_worker if page_read else
                              read_worker if action in READ_ACTIONS else learning_worker)
                    if action in CACHED_READ_ACTIONS:
                        key = json.dumps(body, sort_keys=True, separators=(',', ':'))
                        response = read_cache.request(key, lambda: worker.request(body))
                    else:
                        response = worker.request(body)
                    if response.get('ok') and action not in READ_ACTIONS:
                        read_cache.invalidate()
                    finished = time.monotonic()
                    refresh_inventory = response.get('ok') and (focus_change or body.get('action') in {'queue','target','queue-topic','submit','expire','start','study-topic','review-topic','regenerate-assessment'} or body.get('action') == 'continue' and response.get('data', {}).get('status') in {'completed','failed'}) and not developer_mode(mode_path)
                if response.get("ok"):
                    if review_outbox and not developer_mode(mode_path):
                        response['data'] = review_outbox.decorate(response['data'])
                    self.send_bytes(200, json.dumps(response["data"], separators=(",", ":")).encode(), "application/json; charset=utf-8")
                    if response['data'].get('type') == 'review' and body.get('action') in {'start','review-topic','resume','task'}:
                        # Refresh a long-idle feedback peer while the learner
                        # reads, rather than on their first Check answer click.
                        def warm_review(task_id=response['data']['taskId']):
                            try:
                                feedback_worker.request({'action':'review-session','taskId':task_id})
                            except (OSError, ValueError):
                                pass
                        threading.Thread(target=warm_review, daemon=True).start()
                    if refresh_inventory:
                        inventory_refresh.set()
                else:
                    self.log_error("Learning request failed (%s)", response.get("code", "validation"))
                    self.send_bytes(503 if response.get("code") == "unavailable" else 409, json.dumps({"error": response.get("error", "The request could not be completed."), "code": response.get("code", "validation")}).encode(), "application/json; charset=utf-8")
                if body.get('action') in MUTATING_ACTIONS:
                    print(f"Learning request {body.get('action')} {body.get('requestId', '')}: admission={(admitted-request_started)*1000:.1f} ms worker={(finished-admitted)*1000:.1f} ms total={(time.monotonic()-request_started)*1000:.1f} ms", file=sys.stderr)
            except (subprocess.SubprocessError, OSError, ValueError) as error:
                self.log_error("Learning request failed (%s)", type(error).__name__)
                self.log_error("Learning %s request ended after %.1f ms", body.get('action'), (time.monotonic()-request_started)*1000)
                self.send_bytes(503, b'{"error":"Could not reach the local learning database. Retry the same request."}', "application/json")

        def mode_request(self, body: dict | None = None) -> None:
            try:
                if body is None:
                    # save_json atomically replaces this file. A read does not
                    # need to wait for the scheduler's durable write lock.
                    self.send_bytes(200, json.dumps({"enabled": developer_mode(mode_path), "pausedTasks": []}).encode(), "application/json")
                    return
                request_directory.mkdir(parents=True, exist_ok=True)
                with (request_directory / "api.lock").open("a") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    enabled = developer_mode(mode_path)
                    paused = []
                    if body is not None:
                        desired = body.get("enabled")
                        request = body.get("requestId", "")
                        if type(desired) is not bool or not isinstance(request, str) or not (8 <= len(request) <= 60) or not all(c.isascii() and (c.isalnum() or c == "-") for c in request):
                            self.send_bytes(400, b'{"error":"A boolean enabled value and stable requestId are required."}', "application/json")
                            return
                        if desired and not enabled:
                            if review_outbox:
                                review_outbox.drain(pause_active=True)
                            if learning_worker is None:
                                raise ValueError("Learning API is unavailable")
                            active = learning_worker.request({"action": "preview-active-tasks"})
                            if not active.get("ok"):
                                raise ValueError("Unable to check running activity")
                            for task in active["data"]["taskIds"]:
                                response = learning_worker.request({"action": "pause", "taskId": task, "requestId": f"dev-{request}-{task}"})
                                if not response.get("ok"):
                                    self.send_bytes(409, json.dumps({"error": response.get("error", "Pause the running lesson before enabling developer mode."), "code": response.get("code", "validation")}).encode(), "application/json")
                                    return
                                paused.append(task)
                        if desired != enabled:
                            save_developer_mode(mode_path, desired)
                            enabled = desired
                    self.send_bytes(200, json.dumps({"enabled": enabled, "pausedTasks": paused}).encode(), "application/json")
            except (OSError, ValueError, KeyError, TypeError):
                self.send_bytes(503, b'{"error":"Developer mode could not be confirmed. Activity recording is unavailable until the setting can be read."}', "application/json")

        def graph_preferences_request(self, changes=None) -> None:
            try:
                value = (read_preferences(graph_preferences_path) if changes is None else
                         update_preferences(graph_preferences_path, changes, save_json))
                self.send_bytes(200, json.dumps(value).encode(), 'application/json')
            except ValueError as error:
                self.send_bytes(400, json.dumps({'error': str(error)}).encode(), 'application/json')
            except OSError:
                self.send_bytes(503, b'{"error":"Could not sync display settings. Retry shortly."}', 'application/json')

        def do_POST(self) -> None:
            if not self.trusted():
                return
            action = urlsplit(self.path).path.removeprefix("/api/")
            # Profile preferences remain editable in inspection mode; study writes do not.
            if action not in MUTATING_ACTIONS | {"review-save-retry", "developer-mode", "preview-answer", "profile-settings", "daily-xp-goal", "focused-mode", "graph-preferences"}:
                self.send_bytes(404, b"Not found", "text/plain")
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 128_000 or self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
                    raise ValueError("Expected a JSON request below 128 KB")
                body = json.loads(self.rfile.read(size))
                if not isinstance(body, dict):
                    raise ValueError("Expected a JSON object")
                if action == 'graph-preferences' and not isinstance(body.get('changes'), dict):
                    raise ValueError('Expected graph display changes')
                body["action"] = action
            except (ValueError, TypeError) as error:
                self.send_bytes(400, json.dumps({"error": str(error)}).encode(), "application/json")
                return
            if action == 'graph-preferences':
                self.graph_preferences_request(body.get('changes', {}))
            elif action == "developer-mode":
                self.mode_request(body)
            else:
                self.learning_request(body)

        def do_GET(self) -> None:
            if not self.trusted():
                return
            path = urlsplit(self.path).path
            query = parse_qs(urlsplit(self.path).query)
            if path == '/api/graph-preferences':
                self.graph_preferences_request()
            elif path == "/api/developer-mode":
                self.mode_request()
            elif path == "/api/review-save-status":
                try:
                    task_id = int(query.get("taskId", [""])[0])
                    self.learning_request({"action":"review-save-status", "taskId":task_id})
                except (ValueError, TypeError):
                    self.send_bytes(400, b'{"error":"A task ID is required"}', "application/json")
            elif path == "/api/profile":
                self.learning_request({"action": "profile"})
            elif path == "/api/learner":
                self.learning_request({"action": "learner"})
            elif path == "/api/topic-study-availability":
                try:
                    values = query.get("topicId", [])
                    if len(values) != 1 or not 0 < int(values[0]) <= 9_007_199_254_740_991:
                        raise ValueError("One topic entity ID is required")
                    topic = int(values[0])
                except ValueError:
                    self.send_bytes(400, b'{"error":"One topic entity ID is required."}', "application/json")
                    return
                self.learning_request({"action": "topic-study-availability", "topicId": topic})
            elif path == "/api/preview-home":
                self.learning_request({"action": "preview-home"})
            elif path == "/api/preview":
                try:
                    keys = ("activityId", "taskId", "topicId")
                    if any(key in query and len(query[key]) != 1 for key in keys):
                        raise ValueError("Provide one selector")
                    selectors = {key: int(query[key][0]) for key in keys if key in query}
                    if len(selectors) != 1 or any(value <= 0 for value in selectors.values()):
                        raise ValueError("One activityId, taskId, or topicId is required")
                except ValueError:
                    self.send_bytes(400, b'{"error":"One activityId, taskId, or topicId is required."}', "application/json")
                    return
                self.learning_request({"action": "preview", **selectors})
            elif path == "/api/inventory":
                self.learning_request({"action": "inventory"})
            elif path == "/api/home":
                self.learning_request({"action": "home"})
            elif path in ("/api/study-stats", "/api/forecast-inputs"):
                try:
                    boundaries = query.get("dayStarts", [])
                    if len(boundaries) != 1 or len(boundaries[0]) > 160:
                        raise ValueError("Provide local day boundaries")
                    days = [int(value) for value in boundaries[0].split(",")]
                    if len(days) != 8:
                        raise ValueError("Provide eight local day boundaries")
                except ValueError:
                    self.send_bytes(400, b'{"error":"Provide eight local day boundaries."}', "application/json")
                    return
                self.learning_request({"action": "forecast-inputs" if path == "/api/forecast-inputs" else "study-stats", "dayStarts": days})
            elif path == "/api/assignments":
                self.learning_request({"action": "assignments"})
            elif path == "/api/assignment":
                identifiers = parse_qs(urlsplit(self.path).query, keep_blank_values=True).get("assignment", [])
                if len(identifiers) != 1 or not identifiers[0] or len(identifiers[0]) > 128:
                    self.send_bytes(400, b'{"error":"Provide one assignment identifier."}', "application/json")
                    return
                self.learning_request({"action": "assignment", "assignmentId": identifiers[0]})
            elif path == "/api/activity":
                body = {"action": "activity-history"}
                activity_query = parse_qs(urlsplit(self.path).query, keep_blank_values=True)
                for key in ("taskId", "beforeTaskId"):
                    if key in activity_query:
                        try:
                            values = activity_query[key]
                            if len(values) != 1 or not values[0].isdigit() or not 0 < int(values[0]) <= 2**64 - 1:
                                raise ValueError()
                            body[key] = int(values[0])
                        except ValueError:
                            self.send_bytes(400, b'{"error":"Provide one positive activity identifier."}', "application/json")
                            return
                if "taskId" in body:
                    if "beforeTaskId" in body:
                        self.send_bytes(400, b'{"error":"Provide an activity or a history cursor."}', "application/json")
                        return
                    body["action"] = "activity-history-detail"
                self.learning_request(body)
            elif path == "/api/task":
                try:
                    task = int(query.get("taskId", [""])[0])
                except ValueError:
                    self.send_bytes(400, b'{"error":"taskId is required"}', "application/json")
                    return
                self.learning_request({"action": "task", "taskId": task})
            elif path == "/api/asset":
                asset = image_path(query.get("path", [""])[0], math_root)
                if asset is None:
                    self.send_bytes(404, b"Image not found", "text/plain")
                else:
                    self.send_bytes(200, asset.read_bytes(), IMAGE_TYPES[asset.suffix.lower()], cache=True)
            elif path == "/api/source":
                source = Path(query.get("path", [""])[0]).resolve()
                if source.suffix.lower() != ".pdf" or not any(source.is_relative_to(root.resolve()) for root in ASSET_ROOTS) or not source.is_file():
                    self.send_bytes(404, b"Source PDF not found", "text/plain")
                else:
                    self.send_bytes(200, source.read_bytes(), "application/pdf", cache=True)
            elif path in ("/home", "/learn"):
                self.send_bytes(200, (ROOT / "ui/Learning.html").read_bytes(), "text/html; charset=utf-8")
            elif path in ("/progress", "/course", "/courses"):
                self.send_bytes(200, (ROOT / "ui/Course.html").read_bytes(), "text/html; charset=utf-8")
            elif path == "/topic":
                self.send_bytes(200, (ROOT / "ui/Topic.html").read_bytes(), "text/html; charset=utf-8")
            elif path == "/activity":
                self.send_bytes(200, (ROOT / "ui/Activity.html").read_bytes(), "text/html; charset=utf-8")
            elif path == "/assignments":
                self.send_bytes(200, (ROOT / "ui/Assignments.html").read_bytes(), "text/html; charset=utf-8")
            elif path.startswith("/ui/") and path != "/ui/Math-Academy-Graph-Explorer.html":
                asset = (ROOT / path.lstrip("/")).resolve()
                allowed = {"Activity.html", "activity.js", "activity.css", "learning.js", "learning.css", "study-stats.js", "forecast-sidebar.js", "forecast-worker.js", "forecast.js", "route-matrix.css", "question-fields.js", "content-tables.js", "prose-lists.js", "math-protection.js", "equation-groups.js", "equation-groups.css", "mathjax-config.js", "Learning.html", "MA-Logo.svg", "favicon.svg", "navigation.js", "navigation.css", "Course.html", "course.js", "course.css", "Topic.html", "topic.js", "topic.css", "targets.js", "target-scope.js", "target-weeks.js", "targets.css", "Assignments.html", "assignments.js", "assignments.css", "developer-mode.js", "step-menu.js", "entity-menu.js", "topic-menu.js", "profile.js", "course-catalog.js", "course-catalog.css", "requests.js", "graph-preferences.js"}
                if not asset.is_relative_to((ROOT / "ui").resolve()) or not asset.is_file() or not (asset.name in allowed or asset.is_relative_to((ROOT / "ui/vendor").resolve())):
                    self.send_bytes(404, b"Not found", "text/plain")
                else:
                    self.send_bytes(200, asset.read_bytes(), mimetypes.guess_type(asset)[0] or "application/octet-stream", cache=True)
            elif path in ("/api/graph-explorer", "/api/course", "/api/topic"):
                if self.headers.get("Sec-Fetch-Site") == "cross-site":
                    self.send_bytes(403, b"Forbidden", "text/plain; charset=utf-8")
                    return
                try:
                    request = {}
                    if path == "/api/course":
                        request["action"] = "course"
                        if "course" in query:
                            if len(query["course"]) != 1 or len(query["course"][0]) > 128:
                                self.send_bytes(400, b'{"error":"Provide one course identifier."}', "application/json; charset=utf-8")
                                return
                            request["courseId"] = query["course"][0]
                    elif path == "/api/topic":
                        identifiers = parse_qs(urlsplit(self.path).query, keep_blank_values=True).get("topic", [])
                        if len(identifiers) != 1 or not identifiers[0] or len(identifiers[0]) > 128:
                            self.send_bytes(400, b'{"error":"Provide one topic identifier."}', "application/json; charset=utf-8")
                            return
                        request = {"action": "topic", "topicId": identifiers[0]}
                    key = 'graph:' + json.dumps(request, sort_keys=True, separators=(',', ':'))
                    result = read_cache.request(key, lambda: graph_worker.request(request))
                    if not result.get("ok"):
                        if result.get("code") == "not-found":
                            label = "Topic" if path == "/api/topic" else "Course"
                            self.send_bytes(404, json.dumps({"error": f"{label} not found.", "code": "not-found"}).encode(), "application/json; charset=utf-8")
                            return
                        raise OSError("The graph reader could not capture current data")
                    data = result['data']
                    if path == '/api/graph-explorer':
                        preference = focused_mode(focused_mode_path(request_directory, learner))
                        if preference is not None:
                            data = {**data, 'studyDefaults': {**data.get('studyDefaults', {}),
                                'targetPrerequisiteDepth': 0 if preference else 2}}
                    self.send_bytes(200, json.dumps(data, separators=(",", ":")).encode(), "application/json; charset=utf-8", cache=True)
                except (subprocess.SubprocessError, OSError, ValueError) as error:
                    self.log_error("EDB read failed (%s)", type(error).__name__)
                    if isinstance(error, subprocess.CalledProcessError):
                        print(error.stderr.decode(errors="replace").strip(), file=sys.stderr)
                    self.send_bytes(503, json.dumps({
                        "error": "Could not read EDB. Check the local database and server terminal, then refresh."
                    }).encode(), "application/json; charset=utf-8")
            elif path in ("/", "/Math-Academy-Graph-Explorer.html", "/ui/Math-Academy-Graph-Explorer.html"):
                self.send_bytes(200, HTML.read_bytes(), "text/html; charset=utf-8")
            else:
                # Exact route allowlist: no directory listings, source, or private files.
                self.send_bytes(404, b"Not found", "text/plain; charset=utf-8")

        def do_HEAD(self) -> None:
            self.do_GET()

    Handler.workers = (graph_worker, learning_worker, page_worker, stats_worker, scheduler_worker, feedback_worker, persistence_worker, read_worker, forecast_worker)
    Handler.scheduler_stop = scheduler_stop
    Handler.mark_generator_interruption = staticmethod(inventory_jobs.mark_service_interruption)
    Handler.inventory_refresh = inventory_refresh
    Handler.inventory_ready = inventory_ready
    Handler.read_cache = read_cache
    Handler.background = (scheduler_loop, review_outbox.loop, *(build_loop(slot) for slot in range(builder_count)),
                          generator_refill_loop, inventory_refresh_loop) if learning_worker else ()
    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--database", default=os.environ.get("EDB_DATABASE", DEFAULT_DATABASE))
    parser.add_argument("--learner", default=DEFAULT_LEARNER)
    parser.add_argument("--edb-root", type=Path, default=Path(os.environ.get("EDB_ROOT", ROOT.parent / "EDB")))
    args = parser.parse_args()
    try:
        reader = build_reader(args.edb_root.resolve())
        learning = build_learning(args.edb_root.resolve())
        environment = database_environment(args.database)
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler(reader, args.database, args.learner, environment, learning))
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Cannot start graph explorer: {error}\n")
    print(f"Graph explorer: http://127.0.0.1:{server.server_port}/", flush=True)
    def warm(worker, body):
        try:
            worker.request(body)
        except (OSError, ValueError):
            pass  # A foreground request retries startup and reports any failure.
    for worker, body in zip(server.RequestHandlerClass.workers, ({}, {"action": "profile"}, {"action": "activity-history"}, {"action": "activity-history"}, {"action": "profile"}, {"action": "profile"}, {"action": "profile"}, {"action": "profile"}, {"action": "activity-history"})):
        if worker:
            threading.Thread(target=warm, args=(worker, body), daemon=True).start()
    def stop(_signum, _frame):
        server.RequestHandlerClass.scheduler_stop.set()
        server.RequestHandlerClass.mark_generator_interruption()
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    for background in server.RequestHandlerClass.background:
        if background.__name__ in {'generator_build_loop', 'generator_refill_loop'} and environment.get('COURSE_ACADEMY_DISABLE_GENERATION') == '1':
            continue
        threading.Thread(target=background, daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.RequestHandlerClass.scheduler_stop.set()
        server.server_close()
        for worker in server.RequestHandlerClass.workers:
            if worker:
                worker.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Serve the graph explorer and durable learner app on http://127.0.0.1:8765.

Run: python3 scripts/serve_graph_explorer.py
Uses the local edb_peer PostgreSQL role unless EDB_POSTGRES_URL is supplied.
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
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "ui" / "Math-Academy-Graph-Explorer.html"
SOURCE = ROOT / "scripts" / "graph_explorer_reader.rs"
DEFAULT_LEARNER = "59d5cf13-351c-4114-be19-4c3bb64ee051"
ASSET_ROOTS = (ROOT.parent / "MA/DATA/Lessons", ROOT.parent / "study/vault")
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml"}
MUTATING_ACTIONS = {"start", "answer", "continue", "pause", "resume", "target", "queue",
                    "assignment-focus", "assignment-answer", "assignment-pause"}


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
    sources = (source, ROOT / "scripts/assignment_reader.rs", ROOT / "scripts/assignment_interaction.rs",
               ROOT / "scripts/developer_preview.rs")
    if test:
        sources += (ROOT / "scripts/assignment_interaction_tests.rs",)
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
    sources = (SOURCE, ROOT / "scripts/topic_reader.rs")
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
    graph_worker = NativeWorker([str(reader), database, learner, "--serve"], environment, "graph-worker")
    learning_worker = NativeWorker([str(learning), database, learner, environment["EDB_ENDPOINT"], "--serve"], environment, "learning-worker") if learning else None
    request_directory = Path(environment["LEARNING_REQUEST_DIR"])
    mode_path = request_directory / "developer-mode.json"

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
            allowed_hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            origin = self.headers.get("Origin")
            if host not in allowed_hosts or (origin and origin != f"http://{host}"):
                self.send_bytes(403, b"Forbidden", "text/plain; charset=utf-8")
                return False
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                self.send_bytes(403, b"Forbidden", "text/plain; charset=utf-8")
                return False
            return True

        def learning_request(self, body: dict) -> None:
            if learning_worker is None:
                self.send_bytes(503, b'{"error":"Learning API is unavailable."}', "application/json")
                return
            try:
                directory = Path(environment["LEARNING_REQUEST_DIR"])
                directory.mkdir(parents=True, exist_ok=True)
                # Shared across request threads and server processes. Native writes also
                # compare the EDB basis, covering writers outside this application.
                with (directory / "api.lock").open("a") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX)
                    if body.get("action") in MUTATING_ACTIONS and developer_mode(mode_path):
                        self.send_bytes(409, b'{"error":"Developer mode is on. No activity or learner changes are recorded.","code":"developer-mode"}', "application/json")
                        return
                    if body.get("action") == "assignment":
                        # The server setting selects inspection-only answer keys;
                        # a request cannot promote itself into developer mode.
                        body = {**body, "preview": developer_mode(mode_path)}
                    body = assignment_request(body, directory, learner)
                    response = learning_worker.request(body)
                if response.get("ok"):
                    self.send_bytes(200, json.dumps(response["data"], separators=(",", ":")).encode(), "application/json; charset=utf-8")
                else:
                    self.log_error("Learning request failed (%s)", response.get("code", "validation"))
                    self.send_bytes(503 if response.get("code") == "unavailable" else 409, json.dumps({"error": response.get("error", "The request could not be completed."), "code": response.get("code", "validation")}).encode(), "application/json; charset=utf-8")
            except (subprocess.SubprocessError, OSError, ValueError) as error:
                self.log_error("Learning request failed (%s)", type(error).__name__)
                self.send_bytes(503, b'{"error":"Could not reach the local learning database. Retry the same request."}', "application/json")

        def mode_request(self, body: dict | None = None) -> None:
            try:
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

        def do_POST(self) -> None:
            if not self.trusted():
                return
            action = urlsplit(self.path).path.removeprefix("/api/")
            # Profile preferences remain editable in inspection mode; study writes do not.
            if action not in MUTATING_ACTIONS | {"developer-mode", "preview-answer", "profile-settings"}:
                self.send_bytes(404, b"Not found", "text/plain")
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 128_000 or self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
                    raise ValueError("Expected a JSON request below 128 KB")
                body = json.loads(self.rfile.read(size))
                if not isinstance(body, dict):
                    raise ValueError("Expected a JSON object")
                body["action"] = action
            except (ValueError, TypeError) as error:
                self.send_bytes(400, json.dumps({"error": str(error)}).encode(), "application/json")
                return
            if action == "developer-mode":
                self.mode_request(body)
            else:
                self.learning_request(body)

        def do_GET(self) -> None:
            if not self.trusted():
                return
            path = urlsplit(self.path).path
            query = parse_qs(urlsplit(self.path).query)
            if path == "/api/developer-mode":
                self.mode_request()
            elif path == "/api/profile":
                self.learning_request({"action": "profile"})
            elif path == "/api/preview-home":
                self.learning_request({"action": "preview-home"})
            elif path == "/api/preview":
                try:
                    selectors = {key: int(query[key][0]) for key in ("activityId", "taskId") if key in query and len(query[key]) == 1}
                    if len(selectors) != 1 or any(value <= 0 for value in selectors.values()):
                        raise ValueError("One activityId or taskId is required")
                except ValueError:
                    self.send_bytes(400, b'{"error":"One activityId or taskId is required."}', "application/json")
                    return
                self.learning_request({"action": "preview", **selectors})
            elif path == "/api/home":
                self.learning_request({"action": "home"})
            elif path == "/api/assignments":
                self.learning_request({"action": "assignments"})
            elif path == "/api/assignment":
                identifiers = parse_qs(urlsplit(self.path).query, keep_blank_values=True).get("assignment", [])
                if len(identifiers) != 1 or not identifiers[0] or len(identifiers[0]) > 128:
                    self.send_bytes(400, b'{"error":"Provide one assignment identifier."}', "application/json")
                    return
                self.learning_request({"action": "assignment", "assignmentId": identifiers[0]})
            elif path == "/api/task":
                try:
                    task = int(query.get("taskId", [""])[0])
                except ValueError:
                    self.send_bytes(400, b'{"error":"taskId is required"}', "application/json")
                    return
                self.learning_request({"action": "task", "taskId": task})
            elif path == "/api/asset":
                asset = Path(query.get("path", [""])[0]).resolve()
                if asset.suffix.lower() not in IMAGE_TYPES or not any(asset.is_relative_to(root.resolve()) for root in ASSET_ROOTS) or not asset.is_file():
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
            elif path == "/assignments":
                self.send_bytes(200, (ROOT / "ui/Assignments.html").read_bytes(), "text/html; charset=utf-8")
            elif path.startswith("/ui/") and path != "/ui/Math-Academy-Graph-Explorer.html":
                asset = (ROOT / path.lstrip("/")).resolve()
                allowed = {"learning.js", "learning.css", "mathjax-config.js", "Learning.html", "MA-Logo.svg", "favicon.svg", "navigation.js", "navigation.css", "Course.html", "course.js", "course.css", "Topic.html", "topic.js", "topic.css", "targets.js", "targets.css", "Assignments.html", "assignments.js", "assignments.css", "developer-mode.js", "step-menu.js", "profile.js", "course-catalog.js", "course-catalog.css"}
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
                    result = graph_worker.request(request)
                    if not result.get("ok"):
                        if result.get("code") == "not-found":
                            label = "Topic" if path == "/api/topic" else "Course"
                            self.send_bytes(404, json.dumps({"error": f"{label} not found.", "code": "not-found"}).encode(), "application/json; charset=utf-8")
                            return
                        raise OSError("The graph reader could not capture current data")
                    self.send_bytes(200, json.dumps(result["data"], separators=(",", ":")).encode(), "application/json; charset=utf-8", cache=True)
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

    Handler.workers = (graph_worker, learning_worker)
    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--database", default=os.environ.get("EDB_DATABASE", "course-academy-v2"))
    parser.add_argument("--learner", default=DEFAULT_LEARNER)
    parser.add_argument("--edb-root", type=Path, default=Path(os.environ.get("EDB_ROOT", ROOT.parent / "EDB")))
    args = parser.parse_args()
    try:
        reader = build_reader(args.edb_root.resolve())
        learning = build_learning(args.edb_root.resolve())
        environment = os.environ.copy()
        environment.setdefault("EDB_POSTGRES_URL", f"host={ROOT / '.local/edb/run'} dbname=course_academy user=edb_peer sslmode=disable")
        environment.setdefault("EDB_CONNECT_TIMEOUT_MS", "5000")
        environment.setdefault("EDB_STATEMENT_TIMEOUT_MS", "15000")
        environment.setdefault("EDB_ENDPOINT", "/tmp/course-academy-edb-v2/writer.sock")
        environment.setdefault("LEARNING_REQUEST_DIR", str(ROOT / ".local/learning/requests" / args.database))
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler(reader, args.database, args.learner, environment, learning))
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Cannot start graph explorer: {error}\n")
    print(f"Graph explorer: http://127.0.0.1:{server.server_port}/", flush=True)
    def warm(worker, body):
        try:
            worker.request(body)
        except (OSError, ValueError):
            pass  # A foreground request retries startup and reports any failure.
    for worker, body in zip(server.RequestHandlerClass.workers, ({}, {"action": "home"})):
        if worker:
            threading.Thread(target=warm, args=(worker, body), daemon=True).start()
    def stop(_signum, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        for worker in server.RequestHandlerClass.workers:
            if worker:
                worker.close()


if __name__ == "__main__":
    main()

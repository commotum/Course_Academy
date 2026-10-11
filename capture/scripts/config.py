"""Explicit per-account settings; shared database and image library."""
from __future__ import annotations

from dataclasses import dataclass, field, fields
import os
from pathlib import Path

from .storage import read_json


@dataclass
class Config:
    repo_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    account: str = "foundations"
    state_root: Path | None = None
    output_root: Path | None = None
    math_root: Path = Path("/media/jake/SSD/EDB/math")
    edb_bin: Path | None = None
    endpoint: str = "/tmp/edb-math/writer.sock"
    database: str = "math"
    postgres_url: str = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"
    source: str = ":org/Math-Academy"
    derived_source: str | None = None
    profile: Path | None = None
    course_id: str | None = None
    headless: bool = True
    timeout_ms: int = 30000
    solver_command: list[str] | None = None
    codex_bin: str = "codex"
    solver_model: str | None = None
    solver_timeout: float = 180.0
    solver_attempts: int = 2
    retry_delay: float = 2.0
    recovery_max_delay: float = 60.0
    targets: list[str] = field(default_factory=list)
    seed: int | None = None
    capture_only: bool = False
    browser_cdp_url: str | None = None
    learner_id: str = "59d5cf13-351c-4114-be19-4c3bb64ee051"

    def __post_init__(self):
        self.repo_root = Path(self.repo_root).resolve()
        if not self.account or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in self.account):
            raise ValueError("Account name must contain letters, digits, hyphens, or underscores")
        self.state_root = Path(self.state_root or self.repo_root / ".local/capture" / self.account).resolve()
        self.output_root = Path(self.output_root or self.repo_root / "reference/mathacademy/capture" / self.account).resolve()
        self.math_root = Path(self.math_root).resolve()
        self.edb_bin = Path(self.edb_bin or os.environ.get("EDB_BIN", self.repo_root / ".local/edb/capture-runtime/math-edb")).resolve()
        old_state = self.repo_root / ".local" / ("question_capture" if self.account == "foundations" else "question_capture-workers/" + self.account)
        self.profile = Path(self.profile or old_state / "browser-profile").resolve()
        auth = read_json(old_state / "profile-auth.json", {})
        defaults = {"foundations": "154", "linear": "55", "multivariable": "54", "differential": "61"}
        self.course_id = str(self.course_id or auth.get("course_id") or defaults.get(self.account) or "") or None
        self.targets = list(dict.fromkeys(map(str, self.targets)))
        if self.source != ":org/Math-Academy":
            raise ValueError("Original captured content must use :org/Math-Academy")
        if self.timeout_ms <= 0 or self.solver_timeout <= 0 or self.retry_delay <= 0:
            raise ValueError("Timeouts and retry delays must be positive")

    @property
    def database_lock(self):
        return self.repo_root / ".local/capture/database.lock"

    @property
    def spool_root(self):
        return self.repo_root / "reference/mathacademy/capture-database"

    @classmethod
    def from_file(cls, path, **overrides):
        data = read_json(path, {}) if path else {}
        known = {f.name for f in fields(cls)}
        unexpected = set(data) - known
        if unexpected:
            raise ValueError("Unknown configuration fields: " + ", ".join(sorted(unexpected)))
        data.update({k: v for k, v in overrides.items() if v is not None})
        return cls(**data)

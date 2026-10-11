"""Explicit per-account settings; shared database and image library."""
from __future__ import annotations

from dataclasses import dataclass, field, fields
import math
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
    preview_bin: Path | None = None
    endpoint: str = "/tmp/edb-math/writer.sock"
    database: str = "math"
    postgres_url: str = "host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"
    source: str = ":org/Math-Academy"
    derived_source: str | None = None
    profile: Path | None = None
    course_id: str | None = None
    headless: bool = True
    timeout_ms: int = 45000
    ui_delay_ms: int = 500
    settle_ms: int = 1000
    event_min: float = 0.8
    event_max: float = 2.5
    answer_min: float = 5.0
    answer_max: float = 12.0
    lesson_min: float = 10.0
    lesson_max: float = 25.0
    rest_min: float = 120.0
    rest_max: float = 360.0
    rest_every: int = 20
    assessment_time_min: float = 0.7
    assessment_time_max: float = 0.85
    capacity_min: float = 30.0
    capacity_max: float = 60.0
    solver_command: list[str] | None = None
    codex_bin: str = "codex"
    solver_model: str | None = None
    solver_timeout: float = 300.0
    solver_attempts: int = 2
    retry_delay: float = 30.0
    recovery_max_delay: float = 180.0
    recovery_jitter: float = 5.0
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
        if self.preview_bin is not None:
            self.preview_bin = Path(self.preview_bin).resolve()
        old_state = self.repo_root / ".local" / ("question_capture" if self.account == "foundations" else "question_capture-workers/" + self.account)
        self.profile = Path(self.profile or old_state / "browser-profile").resolve()
        auth = read_json(old_state / "profile-auth.json", {})
        enrolled = read_json(self.state_root / "current-course.json", {}) or {}
        defaults = {"foundations": "154", "linear": "55", "multivariable": "54", "differential": "61"}
        self.course_id = str(self.course_id or enrolled.get("course_id") or auth.get("course_id") or defaults.get(self.account) or "") or None
        if self.source != ":org/Math-Academy":
            raise ValueError("Original captured content must use :org/Math-Academy")
        if any(not math.isfinite(value) or value <= 0 for value in
               (self.timeout_ms, self.solver_timeout, self.retry_delay, self.recovery_max_delay)):
            raise ValueError("Timeouts and retry delays must be positive")
        if not math.isfinite(self.ui_delay_ms) or self.ui_delay_ms < 500:
            raise ValueError("Browser interaction latency must be at least 500 ms")
        if (not math.isfinite(self.settle_ms) or self.settle_ms < 0
                or not math.isfinite(self.recovery_jitter) or self.recovery_jitter < 0
                or not isinstance(self.rest_every, int) or self.rest_every < 0
                or not isinstance(self.solver_attempts, int) or self.solver_attempts < 1):
            raise ValueError("Invalid settling delay, jitter, rest frequency, or solver attempts")
        for kind in ('event', 'answer', 'lesson', 'rest', 'capacity'):
            low, high = getattr(self, kind + '_min'), getattr(self, kind + '_max')
            if not math.isfinite(low) or not math.isfinite(high) or not 0 <= low <= high:
                raise ValueError('Invalid ' + kind + ' wait range')
        if (not math.isfinite(self.assessment_time_min) or not math.isfinite(self.assessment_time_max)
                or not 0 <= self.assessment_time_min <= self.assessment_time_max <= .95):
            raise ValueError('Assessment time fractions must satisfy 0 <= min <= max <= 0.95')

    @property
    def database_lock(self):
        return self.repo_root / ".local/capture/database.lock"

    @property
    def spool_root(self):
        return self.repo_root / "reference/mathacademy/capture-database"

    @classmethod
    def from_file(cls, path, **overrides):
        data = read_json(path, {}) if path else {}
        if data.pop("targets", None):
            raise ValueError("Configure priority topics in :learner/targets, not capture targets")
        if overrides.pop("targets", None):
            raise ValueError("Configure priority topics in :learner/targets, not capture targets")
        known = {f.name for f in fields(cls)}
        unexpected = set(data) - known
        if unexpected:
            raise ValueError("Unknown configuration fields: " + ", ".join(sorted(unexpected)))
        data.update({k: v for k, v in overrides.items() if v is not None})
        return cls(**data)

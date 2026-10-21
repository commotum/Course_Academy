# Three concurrent generator builders

The application now starts three builder loops and one separate refill loop.
Each builder claims the highest-priority available KP through the existing
authoring, independent review, and publication stages.

Each builder has a durable slot lock, and every job still holds its KP lock.
The queue claim remains serialized under the jobs lock. Together these keep
claims unique, prevent build/refill overlap for a KP, and preserve the limit
across service restarts. Slot zero retains the original worker.lock path, so
the already-running pipeline continues to occupy one slot after deployment.

COURSE_ACADEMY_GENERATOR_BUILD_WORKERS controls the number of builders and
defaults to 3. The existing relevance-v5 admission and ordering apply to every
builder. Approved refill remains independent of agent build/review scope.

Validation: 45 inventory worker tests and 9 service admission tests passed.
The concurrent regression holds three distinct highest-priority KPs active at
once, verifies another server instance cannot acquire their occupied slots,
and confirms remaining jobs stay pending. Service tests cover slot count,
inventory readiness, refresh, developer mode, and generation disable.

Deployment preserved the active pipeline, restored the service's normal shutdown
settings, and returned HTTP 200. Live process inspection confirmed exactly three
inventory builder pipelines: the two power-of-quotient KPs and the integer
negative-one-power KP. Verification used process metadata and local queue files.

[Live builders](live-builders.json) · [Deployment](deployment.json) ·
[Pipeline configuration](../../../generate/README.md)

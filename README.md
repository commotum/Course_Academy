# Course Academy

Run the local study app against the existing EDB database and writer:

```bash
python3 scripts/serve_graph_explorer.py
```

The local installation also runs in the background at startup through the user
service `course-academy.service`. It starts PostgreSQL and the EDB writer first.
It does not open a browser. The service definitions are in
[scripts/systemd](scripts/systemd/).

```bash
systemctl --user status course-academy.service
systemctl --user restart course-academy.service
journalctl --user -u course-academy.service -f
# Turn off automatic startup:
systemctl --user disable course-academy.service
```

Open [Study](http://127.0.0.1:8765/home) for the next five eligible lessons, or
the [Progress](http://127.0.0.1:8765/progress), or the
[knowledge graph](http://127.0.0.1:8765/). Course pages read curriculum metadata
and repetition values from EDB; browsing them leaves the study course unchanged.
Lessons present one item at a time
and save responses, active elapsed time, XP, and FIRe progress to EDB. The current
queue serves lessons; review and assessment scheduling is not yet connected to
this interface. Content without a supported grader or sufficient practice is
excluded from the queue.

Our FIRe implementation is in [engine/rust](engine/rust/). It combines the
published mechanisms with configurable policies chosen for Course Academy.
The goal is a reliable engine of our own, informed by the available evidence;
matching Math Academy's private numerical values is not a requirement.
Earned XP uses our accepted [version-one rules](schema/engine/3-xp-weights.edn):
whole-task accuracy, simple task-specific multipliers, and bonus/penalty bands.
The [XP formula report](reference/xp-docs/earned-xp-formula-report.md) documents
the equations, rounding, examples, and fit to all 168 retained activities.
Start with the [research and implementation report](reference/fire-reconstruction.md),
[history verification](reference/fire-history-analysis.md), and
[data model](reference/fire-data-model.md).

```bash
cargo run -- demo
cargo test
# Optional comparison against the preserved Python implementation:
cargo build
PYTHONDONTWRITEBYTECODE=1 python3 tests/rust_parity.py
# Native EDB boundary (requires the sibling EDB release build):
bash tests/check_rust_edb.sh
```

The Rust library and `fire` binary run without Python. The original Python files
remain as the reference implementation used by differential tests. See the
[Rust API and commands](engine/rust/README.md).

The [schema index](schema/README.md) groups curriculum and learner data separately
from instructional content. FIRe policy settings are in
[schema/engine](schema/engine/). The [reference index](reference/README.md)
links the earlier research and source material.

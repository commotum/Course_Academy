# Course Academy

Run the local study app against the `math` EDB database stored at
`/media/jake/SSD/EDB/math`:

```bash
python3 scripts/serve_graph_explorer.py
```

The app reads PostgreSQL through `/tmp/edb-math` on port `55432` (database
`math`, role `edb_peer`) and writes through `/tmp/edb-math/writer.sock`.
Lesson image paths such as `images/ab/…png` resolve inside the database's
image library. `EDB_POSTGRES_URL`, `EDB_ENDPOINT`, `EDB_DATABASE`, and
`EDB_MATH_ROOT` override these defaults; `EDB_ROOT` selects the EDB source/build
directory. Pending request journals are kept separately for each database.
For a learner without a selected course, choose one from the Study page's
profile settings to populate the lesson queue.

The local installation also runs in the background at startup through the user
service `course-academy.service`. It starts PostgreSQL and the EDB writer first.
It does not open a browser. The service definitions are in
[scripts/systemd](scripts/systemd/).
The math PostgreSQL and writer supervisors reuse already running math processes,
including those used by capture jobs. The legacy PostgreSQL unit remains separate.
To install or update the linked user services:

```bash
systemctl --user link "$PWD/scripts/systemd/course-academy-math-postgres.service" \
  "$PWD/scripts/systemd/course-academy-writer.service" \
  "$PWD/scripts/systemd/course-academy.service"
systemctl --user daemon-reload
systemctl --user restart course-academy-writer.service course-academy.service
```

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

For private remote access, use Tailscale Serve while keeping the app bound to
localhost. Set `COURSE_ACADEMY_PUBLIC_ORIGIN` to the exact HTTPS origin Serve
will use, including its port. The user service reads this setting from
`.local/ui.env`; a manually started server reads it from its environment.
For example, use port 8443 if another app already uses Tailscale's port 443:

```bash
# Replace the hostname with this device's Tailscale DNS name.
mkdir -p .local
printf '%s\n' 'COURSE_ACADEMY_PUBLIC_ORIGIN=https://your-host.your-tailnet.ts.net:8443' > .local/ui.env
systemctl --user daemon-reload
systemctl --user restart course-academy.service
sudo tailscale serve --bg --https=8443 http://127.0.0.1:8765
tailscale serve status
```

On another device connected to the tailnet, open the HTTPS URL with `/home`
appended. Tailnet access rules must allow that device to reach the host on the
chosen HTTPS port. The host must remain awake. Serve's background configuration
persists across reboots. To remove this endpoint, run
`sudo tailscale serve --bg --https=8443 off`.

Entered mathematical answers use our [Rust symbolic checker](reference/symbolic-grader-2026-10-05/README.md).
It proves supported equivalences using exact arithmetic and keeps unresolved
comparisons out of learner progress.

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
# Native EDB boundary (requires the sibling EDB release build):
bash tests/check_rust_edb.sh
```

The Rust library and `fire` binary are the sole FIRe implementation. See the
[Rust API and commands](engine/rust/README.md).

The [schema index](schema/README.md) groups curriculum and learner data separately
from instructional content. FIRe policy settings are in
[schema/engine](schema/engine/). The [reference index](reference/README.md)
links the earlier research and source material.

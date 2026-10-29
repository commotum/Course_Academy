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

After changing EDB or the native writer, rebuild both before restarting the
writer. The build command checks the EDB source first so a new writer cannot
silently retain an older compiled EDB library:

```bash
bash scripts/build_local_edb_writer.sh
# Install the completed build, then restart only the writer:
writer="${EDB_MATH_ROOT:-/media/jake/SSD/EDB/math}/bin/course-academy-transactor"
cp -p "$writer" "$writer.previous"
install -m 755 .local/edb-build/course-academy-transactor "$writer.new"
mv -f "$writer.new" "$writer"
systemctl --user restart course-academy-writer.service
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
and save responses, active elapsed time, XP, and FIRe progress to EDB. Study serves
ordinary lessons and due reviews for topics in global graph layer 30 or above.
Assessments may include eligible learned topics at any layer, including topics
studied through an explicit request. Quizzes and required follow-up practice for
assessment misses remain visible regardless of their topics' layers.
In self-directed mode, new lessons come from `learner/targets`, `learner/queue`,
and their prerequisites through two `topic/next` edges, matching the default
Targets graph scope. Unlearned prerequisites never block an in-scope lesson or
expand this boundary. New topics have no progress record or fewer than one
repetition (below the graph's first color band). A topic at band one or above is
excluded even if its local learned flag is false. Explicit learned status and
completed lessons/reviews also prevent repeat new lessons; retention scheduling
keeps its existing rules.
Content without a supported grader or sufficient fresh practice is skipped
individually, so unavailable earlier lessons never hold up later ones. When their
question banks are replenished, they rejoin the ordinary selection automatically.
Available new lessons favor earlier global layers while interleaving topics by
undirected graph distance from the last three completed lessons/reviews and the
other chosen lessons. Distance contributes at most six layers of preference;
there is no requirement to finish a layer before progressing. Question-generation
demand uses the same bounded scope, including topics whose banks are empty.
Course mode and explicit Study Now retain their separate selection rules.
Equal-priority ordinary reviews fill the five visible slots with graph variety:
the longest-overdue review comes first, followed by topics farthest from the
closest review already selected, using prerequisite links in both directions.
Further ties use overdue age and task ID. Required and ongoing work keep their
positions, as does the optional lesson offered after three ordinary reviews.
Completed failed reviews reduce long-term retention strength but refresh current
memory, so their next ordinary review follows a shorter, positive decay interval
instead of returning immediately. Required remediation keeps its existing gates.

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

Graph Color Code, course and Queue filters, Split by course, and week selection
are shared across local and remote browsers through `.local/graph-preferences.json`.
Open graphs refresh these display settings every five seconds and on focus.
These preferences are local server configuration and are not stored in EDB.

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

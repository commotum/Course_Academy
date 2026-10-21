# Reproduction and validation commands

Run from the supplied workspace. `PY` below is
`/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO` is
`/home/jake/Developer/Course_Academy`; `JOB` is this workspace's parent.
All writes were confined to the workspace. No publication, services, engine
changes, or database writes occurred.

1. Exact review counterexamples (failed before with KeyError; both exit zero
   afterward; stdout/stderr saved as before-* and after-*):

       PYTHONDONTWRITEBYTECODE=1 "$PY" evidence/missing-profile.py --package . --template q-74625
       PYTHONDONTWRITEBYTECODE=1 "$PY" evidence/missing-profile.py --package . --template q-131634

2. Retained finding regression, before repair: exits nonzero with both omitted
   profiles named; see regression-before.stderr. Same command after repair:

       PYTHONDONTWRITEBYTECODE=1 "$PY" checks/source_coverage.py

   Passes: exact source-ID coverage, 17 replays, 85/85 complete source choices,
   17 forced-profile samples, independent visible-system/solution checks, and all
   17 profiles reached by ordinary selection within 39 draws.

3. Runtime snapshot synchronization (the only data repair; keeps the 15 prior
   captured profiles and incorporates both omitted sources):

       PYTHONDONTWRITEBYTECODE=1 "$PY" checks/sync_sources.py

   Source basis advances from 3937 to supplied basis 5370. The prior q-74629
   parenthesis normalization is preserved. No generator mathematical rule,
   authored domain, formatter, or replay solution correction was replaced.

4. Affected checks and small retained-family sample:

       PYTHONDONTWRITEBYTECODE=1 "$PY" checks/validate_repair.py

   Passes 57 independent mathematical checks: 17 replays, 17 profile samples,
   18 controlled records and five seeded batch records. Includes unit, scaled,
   swapped and already-cleared pivots; min/max/zero affine parameters; changed
   target assignments and solution-preserving row changes. Runtime-only
   relocation and deterministic CLI output pass; dependency versions match.
   All five non-source inventory records pass visible math checks.

5. Actual shared delivery filtering:

       "$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty hard --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math

   57 input, 17 original replay duplicates removed, 40 fresh records accepted.

6. Counterfactual and within-template shortcut checks after filtering:

       PYTHONDONTWRITEBYTECODE=1 "$PY" checks/post_delivery.py

   All 15 fixed-bank target controls and all 22 ordinary samples survive. For
   each affected profile and one retained vector profile, all five correct
   assignments remain possible. First/last/shortest/longest/fewest-minus/
   most-minus probes each score exactly 1/5 on the controlled cases, before and
   after filtering. Post-filter content is compared by visible prompt/bank/key
   because the publisher assigns stable IDs. An initial UUID-based comparison
   failed for this reason and was corrected; no runtime change was needed.

7. One batch against the real native learner grader:

       "$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json

   Exit zero: 57 correct responses accepted, 228 alternatives rejected,
   zero unresolved checks and zero database writes. Includes post-delivery
   normalized records and retained source replays.

8. Actual Learning UI rendering:

       "$PY" "$REPO/generate/pipeline/render_preview.py" --input evidence/render-input.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math

   Passes all four repaired-profile replay/sample records. The four full-page
   screenshots were inspected with view_image; see visual-inspection.json.

The regression fixture is the supplied source.json, not the runtime snapshot.
Named regression scripts only read runtime files and write evidence. Build-time
sync_sources.py is deliberately not named in repair-regressions.json.

Limitations: these checks use captured inventory basis 5370. That inventory
omits generation metadata, so historical seed reconstruction is untested. No
defective generated inventory instance is demonstrated by a missing replay
capability. Future live learner history, selection policy and database entity
IDs are unavailable; the selection evidence documents a read-only fresh-learner
support model. Shortcut claims concern the recorded probes, not every possible
learner strategy. Unchanged families also retain the prior independent review's
passing math, grading, scope, rendering and variation evidence.

Targeted repair implemented. Original reviewer reproduction exited 1 with 36/36 frequency leaks (evidence/before-shortcut.jsonl); after repair it exits 0 with 9/36 (evidence/after-shortcut.jsonl). Extra-option signs now independent across unit and swap profiles; unit replacement target also varies. Original full-parameter replay preserved. Runtime manifest reduced to actual dependencies; pinned sympy and removed repository-relative interpreter fallback.

Completed commands:
- context Python -B check_repair.py: pass, 52 identical-bank groups / 208 controlled sign cases.
- context Python -B validate_repair.py: pass, 12 complete source banks, 300 full-row math checks including targeted counterexamples and small fresh sample.
- generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json: 300 accepted, 1200 rejected, no failures.
- shared check_delivery.py with source/inventory and easy: 300 inputs, 270 accepted, 30 duplicates.
- shared render_preview.py: 2 records rendered successfully.

Next: inspect screenshots; check identical-bank witnesses after delivery; verify relocated package; record final results. All author writes remain inside workspace. No publication or database changes.

Completed final checks: all 208 controlled records / 52 identical-bank groups survived delivery; modal sign inference is 50% in each applicable group (evidence/post-delivery-report.json). Both screenshots visually inspected. Relocated five-record CLI output matched; forced sampled-original case uses generalized banks, explicit source replay remains available. check_package.py passed; final check_repair.py passed after this sampling-mode distinction. No remaining author implementation step. Source-replay textual deduplication limit is documented, not concealed. Ready for fresh independent review; no publication performed.
Author-2 milestone (2026-10-22): BLOCKED on runner-owned batch selection, finding 79a24ab401bd284df93a. Read feedback.json and full repair-history.json. Exact reproduction from workspace:
`/home/jake/Developer/Course_Academy/.venv/bin/python -B ../review-1-policy-2-fa94c3c9d1dc4929/reproduce_batch_shortcut.py > evidence/author-2-batch-reproduction.json`
Exit 1; the opposite-outlier-sign shortcut succeeds on 5/5 delivered records. Latest independent review explicitly reports generator counterexamples and passes the prior repair. Existing repair-preflight.json already passes retained finding d02e8980f26ead535fe5; no unchanged checks repeated.
Required action: runner must regenerate its samples.json and enforce the requested acceptance check on the delivered pool, retaining cue-breaking cases through delivery, then obtain fresh independent review. samples.json and runner implementation are outside the writable workspace. No attempt was made to write outside scope. Runtime package, regression scripts, and existing repairs remain unchanged; no substitute batch or proposed handoff created. This blocker supersedes the older ready statement below.


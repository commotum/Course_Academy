Targeted repair implemented. Original reviewer reproduction exited 1 with 36/36 frequency leaks (evidence/before-shortcut.jsonl); after repair it exits 0 with 9/36 (evidence/after-shortcut.jsonl). Extra-option signs now independent across unit and swap profiles; unit replacement target also varies. Original full-parameter replay preserved. Runtime manifest reduced to actual dependencies; pinned sympy and removed repository-relative interpreter fallback.

Completed commands:
- context Python -B check_repair.py: pass, 52 identical-bank groups / 208 controlled sign cases.
- context Python -B validate_repair.py: pass, 12 complete source banks, 300 full-row math checks including targeted counterexamples and small fresh sample.
- generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json: 300 accepted, 1200 rejected, no failures.
- shared check_delivery.py with source/inventory and easy: 300 inputs, 270 accepted, 30 duplicates.
- shared render_preview.py: 2 records rendered successfully.

Next: inspect screenshots; check identical-bank witnesses after delivery; verify relocated package; record final results. All author writes remain inside workspace. No publication or database changes.

Completed final checks: all 208 controlled records / 52 identical-bank groups survived delivery; modal sign inference is 50% in each applicable group (evidence/post-delivery-report.json). Both screenshots visually inspected. Relocated five-record CLI output matched; forced sampled-original case uses generalized banks, explicit source replay remains available. check_package.py passed; final check_repair.py passed after this sampling-mode distinction. No remaining author implementation step. Source-replay textual deduplication limit is documented, not concealed. Ready for fresh independent review; no publication performed.

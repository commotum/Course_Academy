All commands run from this evidence_root. Set PYTHONDONTWRITEBYTECODE=1; package was only read. Python executable: /home/jake/Developer/Course_Academy/.venv/bin/python.

1. python audit.py > audit.log 2>&1 (fresh seeds 73100–73605 by form, source 73071–73079, counterfactual 73661).
2. python <repo>/generate/pipeline/check_delivery.py --input independent-samples.json --source <job>/source/source.json --inventory <job>/source/inventory.json --difficulty easy --output delivery-independent --asset-root assets --math-root /media/jake/SSD/EDB/math
3. Same delivery command with --input runner-batch.json --output delivery-runner --asset-root <job>/outputs-3.
4. <repo>/generate/runs/current/check-engine grader-input.json grader-results.json
5. python <repo>/generate/pipeline/render_preview.py --input render-records.json --output render-all --limit 19 --asset-root assets --asset-root <job>/outputs-3 --math-root /media/jake/SSD/EDB/math
6. python finish_checks.py > finish-checks.log 2>&1 (source raster replay comparison, exact runtime-file relocation, deterministic boundary, normalized delivered cue tests).
7. python pixel_probe.py > pixel-probe.log 2>&1 (all 17 captured image banks; exact ten affected IDs).
8. <repo>/generate/runs/current/check-engine delivered-grader-input.json delivered-grader-results.json
9. python summarize_checks.py > summarize-checks.log 2>&1 (visible worked solutions, controlled dependencies, sampler coverage and faithful selection fixtures).
10. python write_report.py (assembles reports from saved independent results).

<repo> = /home/jake/Developer/Course_Academy
<job> = /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186172038

Source images were inspected before writing source-analysis.json and before reading the package. Full source banks: source-banks.png. No author test results were used as independent checks. Native tools are database-free. Publication preparation was absent, so shared prepare_records ran read-only against basis 5125. Pixel extraction initially included source axes/tick labels; symmetry masking resolved that measurement artifact. Final complete source-bank error is at most 1.1 degrees and does not demonstrate a source correction.

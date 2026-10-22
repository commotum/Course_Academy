All commands run from this evidence directory. PY=/home/jake/Developer/Course_Academy/.venv/bin/python; REPO=/home/jake/Developer/Course_Academy. All package imports used -B or dont_write_bytecode. No package writes, publication or database operations.

Independent source: reread original source.json, generate/principles.md and matched prior source-analysis.json; saved confirmed source-analysis.json before revised package reads. Provenance in provenance.json; changed batch code in implementation.diff.

$PY -B review.py
  Replays all10 complete source profiles; fresh seeds1763,5281,14653,62003,91283,134669;63 exact Fraction-ranked records; all five radio choices/both checkbox responses; mathematical errors0. Declared-only relocation and deterministic replay; runtime positive test succeeds and import scripts failing fixture rejects. Boundary counts0,-1,25; hard difficulty; invalid subset.

$REPO/generate/runs/current/check-engine grader-input.json grader-results.json
  86 accepted,251 rejected,0 unresolved.
$PY -B targeted_review.py
  Nine fresh sampler count/seed controls, exact prior prefix replay, affected pivot and scalar counterfactuals. Retains records and actual-grade inputs. No marginal label failures.
$PY -B targeted_delivery.py
  Actual check_delivery on independently sampled five-record seeds1763,5281,14653 and capacity24 seed5281. All survive. Commands and full stage results in targeted-delivery-results.json.
$REPO/generate/runs/current/check-engine targeted-grader-input.json targeted-grader-results.json
  99 accepted,252 rejected,0 unresolved.

For each name=batch,catalog,fresh:
$PY -B $REPO/generate/pipeline/check_delivery.py --input $name.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-$name --math-root /media/jake/SSD/EDB/math
  Batch5->5; catalog39->39; fresh6->5 (1duplicate). Aggregate targeted49->29 is a dedup stress input; separate batch inputs in targeted-delivery-results.json establish stage preservation.

python3 -B check_batch_decisions.py --input previous-batch.json --report prior-failure-reproduced.json
  Exit1 reproduces old fixed-A defect.
python3 -B check_batch_decisions.py --input batch.json --report current-batch-regression.json
  Exit0. New rule defeats old fixed-A shortcut.
$PY -B relocated/checks/check_batch_decisions.py > retained-check.stdout 2> retained-check.stderr
  Exit0; author checks copied under evidence. Only validate_content JOB input path adjusted for relocation. Its old batch negative control fails and current checks pass, confirming preflight behavior without package writes.
python3 -B audit_delivery.py
  Independent before/after coverage, old-shortcut input, inventory original/gen distinction and read-only selection scenarios; actual selection rules inspected in question_selection.rs and learning.rs.
$REPO/generate/runs/current/check-engine shortcut-grader-input.json shortcut-grader-results.json
  5 accepted,3 rejected. Current old fixed-A strategy accepts1/2.

New strict failing case:
python3 -B check_exclusive_subset.py --input delivery-batch/accepted.json --report exclusive-subset-results.json --native-input exclusive-subset-grader-input.json
  Exit1. Inspect A only and assume C opposite:2/2 correct; complete minimal records in minimal-failing-batch.json.
python3 -B check_exclusive_subset.py --input delivery-catalog/accepted.json --report exclusive-subset-catalog-results.json --native-input exclusive-subset-control-grader-input.json
  Exit0. Same-layout full catalog4/6; two legitimate pair records defeat the strategy.
$PY -B prove_selection_rule.py
  Exit0 proves both distinct two-record combinations admitted by new contrasting_subset force singleton answers. Relevant controlled A-only->A+C pair changes only C; A/B unchanged.
$REPO/generate/runs/current/check-engine exclusive-all-grader-input.json exclusive-grader-results.json
  Batched current2 + catalog6 shortcut cases:6 accepted,2 rejected,0 unresolved. Both actual batch shortcuts accepted; both pair controls rejected.

$PY -B $REPO/generate/pipeline/render_preview.py --input render-records.json --output render --limit 12 --math-root /media/jake/SSD/EDB/math
  Actual unmodified UI,12 records. Earlier default limit6 corrected to12. All screenshots inspected in4 contact sheets; exact HTML and screenshots retained. No rendering errors.

python3 -B finish_report.py
python3 -B verify_evidence.py
  Structured report and schema/reference/hash/count verification. Verdict revise for new fixed-count batch shortcut; other7 checks passed.704 native expectations; package unchanged.

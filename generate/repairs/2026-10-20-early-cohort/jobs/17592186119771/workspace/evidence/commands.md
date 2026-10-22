# Commands and results

Run from the workspace. Python is `/home/jake/Developer/Course_Academy/.venv/bin/python` (3.13.5; SymPy 1.14.0). The following variables only shorten the commands:

```bash
repo=/home/jake/Developer/Course_Academy
py="$repo/.venv/bin/python"
```

The original `"$py" 17592186119771.py --difficulty easy --count 5 --seed 0 --format json` exited 1 with the three-task exhaustion error, preserved in before.stderr. The same command now exits 0 and produces evidence/samples.json.

```bash
"$py" checks/validate.py
"$repo/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json
"$py" "$repo/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$py" "$repo/generate/pipeline/check_delivery.py" --input evidence/samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/sample-delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$py" checks/delivery_probe.py
"$py" "$repo/generate/pipeline/render_preview.py" --input evidence/render-input.json --output evidence/render --asset-root evidence/delivery/assets --math-root /media/jake/SSD/EDB/math
```

Fidelity: 11/11 supplied banks, 55/55 choices, all original key/difficulty/solution presences and absences preserved in evidence-only replay. Prompt and solution comparisons normalize whitespace, math delimiters and harmless TeX braces; visible matrix contents are independently parsed. All 11 source parameter sets also work in normal generation with derived grading keys and solutions. The older bundled snapshot lacked q-13785; it was refreshed from the authoritative supplied evidence, not excluded from replay.

Correctness: all 12 finite easy support patterns tested, with independent zero-region classification of printed matrices and printed witness coordinates. Five-task CLI, deterministic replay, honest 13-task exhaustion, exclusion of seven patterns followed by delivery of exactly the five remaining patterns, 24 controlled records, and three moderate/hard regression examples pass.

Grading: native harness passed 44 accepted and 176 rejected radio submissions. Controlled transpose and clearing cases, plus irrelevant diagonal/sign/letter changes, are included in this same grader batch. No engine changes.

Variation and filtering: shared publisher accepted 36/36 audit records and 5/5 requested samples, with no duplicates. Postdelivery probe rechecks printed content and records label/size/position cue results before and after filtering. Every tested size/letter subgroup contains lower, upper and diagonal answers; no single constant label succeeds throughout any subgroup. Correct positions vary at both sizes. Changing the decisive zero region changes the answer; changing incidental values preserves it. The full structural set includes nonzero witness shifts away from the first cell in 3×3. A fresh-pool reproduction of the native within-band selection formula uses 64 draws with two candidate orders, explicitly substituting UUID order for unavailable future entity IDs. Actual history-sensitive selection is not exercised.

Rendering: the unmodified Learning UI passed three cases with no MathJax, JavaScript, image or font errors. Inspected all three saved screenshots: clear complete matrices, aligned rows/columns, all five readable options, and full worked solutions with correct witnesses; no clipping or overlap observed. The preview's selection annotations are renderer instrumentation.

Relocation: copied exactly the three manifest-listed runtime files into a fresh temporary directory, ran the entrypoint with that directory as cwd and the same five-question command, and compared the complete JSON array to samples.json. It matched; see relocation.json.

Inventory: inspected all 16 captured records; 15 stored keys agree with independent visible-matrix classification. q-13769 lacks a source key and remains ungraded evidence. The demonstrated defect is batch supply, not an incorrect stored classification, so affected-inventory.json is empty. This is a verified lack of per-record applicability of this finding, not a claim that all possible weaknesses were tested. No stored generation metadata was supplied, preventing attribution/replay of historical generated records. Original source questions were not marked generated.

Limits: easy supplies 12 structural patterns; different values do not count as additional structures. Identity and Other are retained distractors within the three existing supported families. Broader classification outcomes are not advertised. The hard band is an existing authored longer scan, not an observed source rating. Live learner history, live database identities, policy configuration and inventory changes after basis 5451 remain untested. All actions were local and database-free; no images were published.

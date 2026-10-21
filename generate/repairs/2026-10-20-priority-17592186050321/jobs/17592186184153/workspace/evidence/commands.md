# Reproduce the author checks

Run from the supplied workspace. Runtime is Python 3.13.5 with no third-party packages. Validation uses the job environment's SymPy 1.14.0 and existing database-free tools.

```bash
/home/jake/Developer/Course_Academy/.venv/bin/python generator.py --difficulty moderate --count 5 --seed 84153 --format json > evidence/sample.json
/home/jake/Developer/Course_Academy/.venv/bin/python generator.py --replay-source > evidence/source-replay.json
/home/jake/Developer/Course_Academy/.venv/bin/python validate.py > evidence/validation-command.txt 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python final_checks.py > evidence/final-checks-command.txt 2>&1
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grading.json > evidence/grading-command.txt 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/test-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math > evidence/delivery-command.txt 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python validate.py --after-delivery > evidence/after-delivery-command.txt 2>&1
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math --limit 8 > evidence/render-command.txt 2>&1
```

The final renderer invocation was run using `evidence/ui-records.json`, containing the same eight mathematical questions as the reproducibly created `evidence/render-records.json` (delivery identities and source replay validation markers differ). The `--limit 8` includes both original moderate radio examples after the six generated representatives. Every screenshot question-001.png through question-008.png was visually inspected after the final bank revision. No clipped mathematics, exposed TeX, malformed fractions/radicals, broken images, or misplaced blank/C were observed. DOM/font/image/MathJax checks passed for all eight.

## Results by claim

* Fidelity: 7 source antiderivatives checked; all 21 captured choices matched; all 4 captured radio banks retained and the 2 moderate source banks reconstructed from recipes. The missing derivative given in q-133291 was restored from its source worked solution. q-71173 and q-113781 have no captured fields and receive math-only replay.
* Correctness: 48 explicit boundaries, 240 normal items, 22 controlled pairs, and a 9-item regression passed independent SymPy differentiation and parsing of the rendered prompt, answer, and solution. Final parameter validation rejects 9 invalid bank assignments. Relocation and deterministic output passed. Equivalent responses and complete radio banks were checked through the actual grader: 115 accepted, 310 rejected, 0 unresolved.
* Delivery: 240 input, 8 duplicates, 232 accepted against captured inventory basis 5277. There are 163 semantic integrand instances, excluding option shuffles, variable names, term order, and distractor-bank variations; the same 163 survive delivery. All supported exponent/sign/constant slots survive. Factor choices, coefficient magnitude ranks, offset signs and all four omitted grid cells are exercised.
* Variation: the initial source-bank extrapolation had a polynomial n=2 length cue (20/21 second-longest successes). New generation uses the explicitly documented P-grid/R-grid authored bank extension; original banks remain available for faithful replay. Length-rank probes now vary for every exponent group and every tested profile/sign/order subgroup. Each radio retains at least two possibilities after solving either individual summand alone. Controlled factor/omission changes vary the bank without changing its correct integral. Relevant sign/exponent/constant changes alter the prompt, correct mathematics, worked solution, and native-grade outcomes together.
* Learner selection: read-only reproduction of the within-band SHA-256 uniform rule used 1,024 synthetic draws from accepted records; P=352, R=371, B=301. Live history, actual database entity ordering, zero moderate weight, concurrent inventory changes, and database identity collisions are outside this offline evidence. The no-policy selector chooses the first eligible database ID, so no claim of live distribution is made.

Moderate is the only supported generation band. Easy lacks labelled source evidence; the hard source lacks its response contract. Unlabelled captured radios remain unlabelled replay evidence and are not silently classified. The package creates no images or assets and performs no writes. Test tools write only local evidence; publication and database changes remain with the runner.
